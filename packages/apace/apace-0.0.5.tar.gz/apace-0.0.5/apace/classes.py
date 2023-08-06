import inspect
import latticejson
import sys
from typing import List, Dict, Set, Union, Iterator
from .utils import Signal, Attribute
from .exceptions import AmbiguousNameError


class Base:
    """Abstract base for all element and lattice classes.

    :param str name: The name of the object.
    :param info: Additional information about the object.
    :type info: str, optional
    """

    def __init__(self, name, length, info=""):
        self.name: str = name
        """The name of the object."""
        self.info: str = info
        """Additional information about the object"""
        self.parent_lattices: Set["Lattice"] = set()
        """All lattices which contain the object."""
        self._length = length

    @property
    def length(self) -> float:
        """Length of the object (m)."""
        return self._length

    def __repr__(self):
        return self.name

    def __str__(self):
        attributes = [("type", self.__class__.__name__)]
        properties = []
        signals = []
        for key in dir(self):
            if key.startswith("_"):
                continue

            obj = getattr(self, key)
            if isinstance(obj, property):
                properties.append(key, str(obj))
            elif isinstance(obj, Signal):
                signals.append((key, str(obj)))
            else:
                attributes.append((key, str(obj)))

        info = attributes + properties + signals
        return "\n".join(f"{name:16}: {string}" for name, string in info)


class Element(Base):
    """Abstract base for all element classes.

    :param str name: The name of the element.
    :param float length: The length of the element (m).
    :param str info: Additional information about the element.
    :type info: str, optional
    """

    def __init__(self, name, length, info=""):
        super().__init__(name, length, info)
        self._length = length
        self.attribute_changed: Signal = Signal()
        """Gets emitted when one of the attributes changes."""
        self.attribute_changed.connect(self._on_attribute_changed)

    @property
    def length(self) -> float:
        """Length of the element (m)."""
        return self._length

    @length.setter
    def length(self, value):
        self._length = value
        self.attribute_changed(self, Attribute.LENGTH)

    def _on_attribute_changed(self, element, attribute):
        for lattice in self.parent_lattices:
            lattice.element_changed(element, attribute)


class Drift(Element):
    """A drift space element.

    :param str name: The name of the element.
    :param float length: The length of the element (m).
    :param str info: Additional information about the element.
    :type info: str, optional
    """

    pass


class Dipole(Element):
    """A dipole element.

    :param str name: Name of the element.
    :param float length: Length of the element (m).
    :param float angle: Deflection angle in rad.
    :param e1: Entrance angle in rad.
    :type e1: float, optional
    :param e2: Exit angle in rad.
    :type e2: float, optional
    :param info: Additional information about the element.
    :type info: str, optional
    """

    def __init__(self, name, length, angle, e1=0, e2=0, info=""):
        super().__init__(name, length, info)
        self._angle = angle
        self._e1 = e1
        self._e2 = e2

    @property
    def angle(self) -> float:
        """Deflection angle (rad)."""
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.attribute_changed(self, Attribute.ANGLE)

    @property
    def e1(self) -> float:
        """Entrance angle (rad)."""
        return self._e1

    @e1.setter
    def e1(self, value):
        self._e1 = value
        self.attribute_changed(self, Attribute.E1)

    @property
    def e2(self) -> float:
        """Exit angle (rad)."""
        return self._e2

    @e2.setter
    def e2(self, value):
        self._e2 = value
        self.attribute_changed(self, Attribute.E2)

    @property
    def radius(self) -> float:
        """Radius of curvature (m)."""
        return self.length / self.angle

    @radius.setter
    def radius(self, value):
        self.angle = self.length / value

    @property
    def k0(self) -> float:
        """Geometric dipole strength or curvature of radius (m)."""
        return self.angle / self.length

    @k0.setter
    def k0(self, value):
        self.angle = value * self.length


class Quadrupole(Element):
    """A quadrupole element.

    :param str name: Name of the element.
    :param float length: Length of the element (m).
    :param float k1: Geometric quadrupole strength (m^-2).
    :param info: Additional information about the element.
    :type info: str, optional
    """

    def __init__(self, name, length, k1, info=""):
        super().__init__(name, length, info)
        self._k1 = k1

    @property
    def k1(self) -> float:
        """Geometric quadrupole strength (m^-2)."""
        return self._k1

    @k1.setter
    def k1(self, value):
        self._k1 = value
        self.attribute_changed(self, Attribute.K1)


class Sextupole(Element):
    """A sextupole element.

    :param str name: Name of the element.
    :param float length: Length of the element (m).
    :param float k1: Geometric quadrupole strength (m^-3).
    :param info: Additional information about the element.
    :type info: str, optional
    """

    def __init__(self, name, length, k2, info=""):
        super().__init__(name, length, info)
        self._k2 = k2

    @property
    def k2(self) -> float:
        """Geometric sextupole strength (m^-3)."""
        return self._k2

    @k2.setter
    def k2(self, value):
        self._k2 = value
        self.attribute_changed(self, Attribute.K2)


class Octupole(Element):
    """An octupole element.

    :param str name: Name of the element.
    :param float length: Length of the element (m).
    :param float k3: Geometric quadrupole strength (m^-4).
    :param info: Additional information about the element.
    :type info: str, optional
    """

    def __init__(self, name, length, k3, info=""):
        super().__init__(name, length, info)
        self._k3 = k3

    @property
    def k3(self) -> float:
        """Geometric sextupole strength (m^-1)."""
        return self._k3

    @k3.setter
    def k3(self, value):
        self._k3 = value
        self.attribute_changed(self, Attribute.K3)


class Lattice(Base):
    """Defines the order of elements in the accelerator.

    :param str name: Name of the lattice.
    :param tree: Nested tree of elements and lattices.
    :type tree: Tuple[Union[Element, Lattice]]
    :param str info: Additional information about the lattice.
    """

    def __init__(self, name, tree, info=None):
        super().__init__(name, info)
        self._tree = tree
        for obj in set(tree):
            obj.parent_lattices.add(self)

        self._objects = {}
        self._elements = set()
        self._sub_lattices = set()
        self._arrangement = []
        self._indices = {}
        self._init_tree_properties()

        self.element_changed: Signal = Signal()
        """Gets emitted when an attribute of an element within this lattice changes."""
        self.element_changed.connect(self._on_element_changed)

        self._length = 0
        self._length_needs_update = True
        self.length_changed: Signal = Signal()
        """Gets emitted when the length of lattice changes."""
        self.length_changed.connect(self._on_length_changed)

        self.n_elements = len(self.arrangement)
        """The number of elements within this lattice."""

    @staticmethod
    def traverse_tree(tree) -> Iterator[Base]:
        "Returns iterator which traverses all nodes of the lattice tree."
        for obj in tree:
            yield obj
            if isinstance(obj, Lattice):
                yield from Lattice.traverse_tree(obj)

    def _init_tree_properties(self):
        """A recursive helper function to initialize the tree properties."""
        arrangement = self._arrangement
        indices = self._indices
        elements = self._elements
        sub_lattices = self._sub_lattices
        objects = self._objects
        index = 0
        for obj in Lattice.traverse_tree(self.tree):
            value = objects.get(obj.name)
            if value is None:
                objects[obj.name] = obj
            elif obj is not value:
                raise AmbiguousNameError(obj.name)

            try:
                indices[obj].append(index)
            except KeyError:
                indices[obj] = [index]

            if isinstance(obj, Lattice):
                sub_lattices.add(obj)
            else:
                arrangement.append(obj)
                elements.add(obj)
                index += 1

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._objects[key]
        elif isinstance(key, (int, slice)):
            return self.arrangement[key]
        elif isinstance(key, Base):
            return self.indices[Base]

    def __del__(self):
        for obj in self.tree:
            obj.parent_lattices.discard(self)

    @property
    def length(self) -> float:
        """Length of the lattice."""
        if self._length_needs_update:
            self.update_length()
        return self._length

    def update_length(self):
        """Manually update the Length of the lattice (m)."""
        # TODO: can numpy be used to avoid rounding errors?
        #       sum = (a + b) + (c + d)
        self._length = sum(obj.length for obj in self.tree)
        self._length_needs_update = False

    def _on_length_changed(self):
        self._length_needs_update = True
        for lattice in self.parent_lattices:
            lattice.length_changed()

    def _on_element_changed(self, element, attribute):
        if attribute == Attribute.LENGTH:
            self.length_changed()

        for lattice in self.parent_lattices:
            lattice.element_changed(element, attribute)

    @property
    def tree(self) -> List[Base]:
        """List of elements and sub-lattices in physical order."""
        return self._tree

    @property
    def arrangement(self) -> List[Element]:
        """List of elements in physical order. (Flattend :attr:`tree`)"""
        return self._arrangement

    @property
    def indices(self) -> Dict[Element, List[float]]:
        """A dict which contains the a `List` of indices for each element.
        Can be thought of as inverse of arrangement. Sub-lattices are associated with
        the list of indices of their first element."""
        return self._indices

    @property
    def objects(self) -> Dict[str, Union[Element, "Lattice"]]:
        """A Mapping from names to the given `Element` or `Lattice` object."""
        return self._objects

    @property
    def elements(self) -> Set[Element]:
        """Unordered set of all elements within this lattice."""
        return self._elements

    @property
    def sub_lattices(self) -> Set["Lattice"]:  # TODO: Python 3.7 change type hint
        """Unordered set of all sub-lattices within this lattice."""
        return self._sub_lattices

    def print_tree(self):
        """Print the lattice as tree of objects. (Similar to unix tree command)"""
        print(self._print_tree(self))

    @staticmethod
    def _print_tree(obj, prefix=""):
        string = f"{obj.name}\n"
        if isinstance(obj, Lattice):
            *others, last = obj.tree
            for child in others:
                string += f"{prefix}├─── {Lattice._print_tree(child, prefix + '│   ')}"
            string += f"{prefix}└─── {Lattice._print_tree(last, prefix + '    ')}"
        return string

    @classmethod
    def from_file(cls, location, file_format=None) -> "Lattice":
        """Creates a new `Lattice` from file at `location` (path or url).
        :param location: path-like or url-like string which locates the lattice file
        :type location: Union[AnyStr, Path]
        :param file_format str: File format of the lattice file
        :type file_format: str, optional (use file extension)
        :rtype Lattice
        """
        return cls.from_dict(latticejson.load(location, file_format))

    @classmethod
    def from_dict(cls, data) -> "Lattice":
        """Creates a new `Lattice` object from a latticeJSON compliant dictionary."""

        objects = {}  # dict containing all elements + lattices
        for name, (type_, attributes) in data["elements"].items():
            class_ = getattr(sys.modules[__name__], type_)
            objects[name] = class_(name=name, **attributes)

        # TODO: make sure sub_lattices are loaded in correct order
        for name, child_names in data["lattices"].items():
            children = [objects[name] for name in child_names]
            objects[name] = Lattice(name, children)

        root_lattice = objects[data["root"]]
        root_lattice.info = data.get("info", "")
        return root_lattice

    def as_file(self, path, file_format=None):
        latticejson.save(self.as_dict(), path, file_format)

    def as_dict(self):
        """Serializes the `Lattice` object into a latticeJSON compliant dictionary."""
        elements_dict = {}
        for element in self.elements:
            type_ = type(element)
            parameters = inspect.signature(type_).parameters.items()
            attributes = {key: getattr(element, key) for (key, value) in parameters}
            name = attributes.pop("name")
            elements_dict[name] = [type_.__name__, attributes]

        lattices_dict = {
            lattice.name: [obj.name for obj in lattice.tree]
            for lattice in self.sub_lattices
        }
        lattices_dict[self.name] = [obj.name for obj in self.tree]

        return dict(
            version="2.0",
            root=self.name,
            info=self.info,
            elements=elements_dict,
            lattices=lattices_dict,
        )
