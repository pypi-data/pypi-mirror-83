""" Classes used for abstract description of LCI data """

import re
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Union, Optional, List, Dict

from eldam.core.parameters import *
from eldam.utils.lci_data import encode_comment, encode_json_data, encode_simapro_csv_format
from eldam.utils.misc import n_float, n_int
from eldam.utils.exceptions import FlowTypeError, MissingParameterError, InputParameterValueError, ProductTypeError
from eldam.utils.xls import extract_variables_from_formula


class InventoryData(metaclass=ABCMeta):
    """ Interface used to specify needed methods """

    @abstractmethod
    def json_data(self):
        pass

    @abstractmethod
    def encoded_comment(self):
        pass

    @abstractmethod
    def simapro_csv_format(self):
        pass


class FlowFactory:
    """ Factory used to create to proper flow object based on its flow type. """

    @staticmethod
    def create_flow(name, type, unit, amount, **kwargs):
        """

        Args:
            name (str):
            type (str):
            unit (str):
            amount:
            **kwargs:

        Returns:
            Flow: Flow based on the proper Flow subclass
        """
        if type in PRODUCT_FLOW_TYPES:
            flow = ProductFlow(name=name, type=type, unit=unit, amount=amount, **kwargs)
        elif type in TECHNOSPHERE_FLOW_TYPES:
            flow = TechnosphereFlow(name=name, type=type, unit=unit, amount=amount, **kwargs)
        elif type in BIOSPHERE_FLOW_TYPES:
            flow = BiosphereFlow(name=name, type=type, unit=unit, amount=amount, **kwargs)
        else:
            raise FlowTypeError(f'{type} is not a recognized flow type.')

        return flow


@dataclass
class Flow(InventoryData, metaclass=ABCMeta):
    """ Abstract class describing a process flow """

    name: str  # Flow name
    type: str  # Flow type
    unit: str  # Flow unit
    amount: Union[str, float]  # Amount or formula if of unknown type
    data_source: Optional[str] = None  # Source of the flow data
    library: Optional[str] = None  # Database the flow comes from
    review_state: int = 0  # State of the review:0: No, 1:Yes with changes, 2:Yes)
    comment_for_reviewer: Optional[str] = None  # Comment for the reviewer
    reviewer_comment: Optional[str] = None  # Reviewer's comment
    comment: Optional[str] = None  # Comment on the flow
    uncertainty: Optional[str] = None  # Uncertainty type
    stdev: Optional[float] = None  # Standard deviation value
    min_value: Optional[float] = None  # Minimum value
    max_value: Optional[float] = None  # Maximum value

    def __post_init__(self):

        if self.uncertainty == 'Undefined':
            self.uncertainty = None
        self.stdev = n_float(self.stdev)
        self.min_value = n_float(self.min_value)
        self.max_value = n_float(self.max_value)

        if type(self.amount) == str:
            if re.match(r'^\d+([,.]\d*)?$', self.amount) is not None:
                self.amount = float(self.amount.replace(',', '.'))
                self.amount_type = 'Value'
            else:
                self.amount_type = 'Formula'
        elif type(self.amount) == float or type(self.amount) == int:
            self.amount_type = 'Value'
        else:
            raise Exception('The amount is neither a string or a numeric value')

    def __repr__(self):
        """
        Example:
            >>> from eldam.core.lci_data import ProductFlow
            >>> str(ProductFlow(name='name', type='Output/Technosphere/Product', unit='unit', amount='A+B+6.5'))
            'name: A+B+6.5 unit'
        """
        return f"{self.name}: {self.amount} {self.unit}"

    @property
    def json_data(self):
        """
        Returns a json encoded string containing every flow data that are not handled by simapro such as review or
        quality data.

        Returns:
            str: Json encoded string

        Examples:
            >>> from eldam.core.lci_data import ProductFlow
            >>> ProductFlow(name='name', type='Output/Technosphere/Product', unit='unit', amount=3, data_source='data_source', library='Ecoinvent',
            ... review_state=2, comment_for_reviewer='Comment for reviewer', reviewer_comment='Reviewer comment').json_data
            '{"data_source": "data_source", "library": "Ecoinvent", "review_state": 2, "reviewer_comment": "Reviewer comment", "comment_for_reviewer": "Comment for reviewer"}'
        """

        return encode_json_data(data_source=self.data_source,
                                library=self.library,
                                review_state=self.review_state,
                                reviewer_comment=self.reviewer_comment,
                                comment_for_reviewer=self.comment_for_reviewer)

    @abstractmethod
    def encoded_comment(self, elda_only_data):
        pass

    @abstractmethod
    def simapro_csv_format(self, elda_only_data):
        pass


@dataclass
class ProductFlow(Flow):
    """ Class used for products and coproducts modelling """
    category: str = 'ELDAM'  # SimaPro category of the flow
    allocation: Optional[str] = None  # Flow allocation percentage, can be a formula
    waste_type: Optional[str] = None  # Product waste type

    def __post_init__(self):
        super().__post_init__()

        if self.type not in PRODUCT_FLOW_TYPES:
            raise FlowTypeError(f'{self.type} is not a recognized product flow type.')

    def __repr__(self):
        return super().__repr__()

    def encoded_comment(self, elda_only_data):
        """
        Returns a string containing the comment, quality data, and json encoded data

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Encoded comment

        Examples:
            >>> print(ProductFlow(name='name2', unit='unit2', type='Output/Technosphere/Product',
            ...         amount=5, review_state=1, comment_for_reviewer='Some comment for reviewer',
            ...         comment='Some comment').encoded_comment(elda_only_data=True))
            Some comment
            <BLANKLINE>
            !!! DO NOT EDIT BELOW THIS LINE !!!
            [[{"review_state": 1, "comment_for_reviewer": "Some comment for reviewer"}]]
            >>> print(ProductFlow(name='name2', unit='unit2', type='Output/Technosphere/Product',
            ...         amount=5, review_state=1, comment_for_reviewer='Some comment for reviewer',
            ...         comment='Some comment').encoded_comment(elda_only_data=False))
            Some comment
        """

        return encode_comment('simple_comment.jinja2',
                              comment=self.comment,
                              json_data=self.json_data if elda_only_data else None)

    def simapro_csv_format(self, elda_only_data):
        """
        Returns a string formatted for insertion in a SimaPro csv import file.

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Formatted string

        Examples:
            >>> print(ProductFlow(name='name2', unit='unit2', type='Output/Technosphere/Product',
            ...         amount=5, review_state=1, comment_for_reviewer='Some comment for reviewer',
            ...         comment='Some comment', allocation=80).simapro_csv_format(elda_only_data=True))
            "name2";"unit2";5;80;"not defined";"ELDAM";"Some comment!!! DO NOT EDIT BELOW THIS LINE !!![[{""review_state"": 1, ""comment_for_reviewer"": ""Some comment for reviewer""}]]"
        """
        if self.type == 'Output/Technosphere/Product':
            waste_type = self.waste_type or "not defined"
            return encode_simapro_csv_format(self.name, self.unit, self.amount, self.allocation or '', waste_type,
                                             self.category, self.encoded_comment(elda_only_data=elda_only_data))

        if self.type == 'Output/Technosphere/Waste treatment product':
            waste_type = self.waste_type or "All waste types"
            return encode_simapro_csv_format(self.name, self.unit, self.amount, waste_type, self.category,
                                             self.encoded_comment(elda_only_data=elda_only_data))


@dataclass
class TechnosphereFlow(Flow):
    """ Class used for modelling of technosphere flows others than products and coproducts flows """
    modification_code: Optional[int] = None  # Flow modification code
    modification_comment: Optional[str] = None  # Flow modification comment
    relevance_code: Optional[str] = None  # Flow relevance code
    relevance_comment: Optional[str] = None  # Flow relevance comment
    confidence_code: Optional[str] = None  # Numeric value confidence code
    confidence_comment: Optional[str] = None  # Numeric value confidence comment

    def __post_init__(self):
        super().__post_init__()

        if self.type not in TECHNOSPHERE_FLOW_TYPES:
            raise FlowTypeError(f'{self.type} is not a recognized technosphere flow type.')

        self.modification_code = n_int(self.modification_code)

    def __repr__(self):
        return super().__repr__()

    def encoded_comment(self, elda_only_data):
        """
        Returns a string containing the comment, quality data, and json encoded data

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Encoded comment

        Examples:
            >>> print(TechnosphereFlow(name='name', type='Input/Technosphere', unit='unit', amount=4,
            ...         modification_code=2, modification_comment='modification_comment', relevance_code='A',
            ...         relevance_comment='relevance comment', confidence_code='Y',
            ...         confidence_comment='confidence comment', comment='general comment', review_state=2,
            ...         reviewer_comment='Reviewer comment').encoded_comment(elda_only_data=True))
            2AY:
            2: modification_comment
            A: relevance comment
            Y: confidence comment
            <BLANKLINE>
            general comment
            <BLANKLINE>
            !!! DO NOT EDIT BELOW THIS LINE !!!
            [[{"review_state": 2, "reviewer_comment": "Reviewer comment"}]]

            If the modification code is 0 or if the relevance code is A, they are only shown on the first line, unless
            their respective comment is not empty.

            >>> print(TechnosphereFlow(name='name', type='Input/Technosphere', unit='unit', amount=4,
            ...         modification_code=0, modification_comment='modification_comment', relevance_code='A',
            ...         confidence_code='Y', confidence_comment='confidence comment', comment='general comment',
            ...         review_state=2, reviewer_comment='Reviewer comment').encoded_comment(elda_only_data=False))
            0AY:
            0: modification_comment
            Y: confidence comment
            <BLANKLINE>
            general comment
        """

        return encode_comment('technosphere_flow_comment.jinja2',
                              modification_code=self.modification_code,
                              modification_comment=self.modification_comment,
                              relevance_code=self.relevance_code,
                              relevance_comment=self.relevance_comment,
                              confidence_code=self.confidence_code,
                              confidence_comment=self.confidence_comment,
                              comment=self.comment,
                              json_data=self.json_data if elda_only_data else None)

    def simapro_csv_format(self, elda_only_data):
        """
        Returns a string formatted for insertion in a SimaPro csv import file.

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Formatted string

        Examples:
            >>> print(TechnosphereFlow(name='name2', unit='unit2', type='Input/Technosphere',
            ...         amount=5, review_state=1, comment_for_reviewer='Some comment for reviewer',
            ...         comment='Some comment', uncertainty='Lognormal', stdev=50).simapro_csv_format(elda_only_data=True))
            "name2";"unit2";5;"Lognormal";50.0;0;0;"Some comment!!! DO NOT EDIT BELOW THIS LINE !!![[{""review_state"": 1, ""comment_for_reviewer"": ""Some comment for reviewer""}]]"
        """

        return encode_simapro_csv_format(self.name, self.unit, self.amount, self.uncertainty or 'Undefined',
                                         self.stdev or 0, self.min_value or 0, self.max_value or 0,
                                         self.encoded_comment(elda_only_data=elda_only_data))

    @property
    def missing_quality_data(self):
        """
        Returns the missing quality data of the flow

        Returns:
            list: A list of the missing attributes names

        Examples:
        >>> print(TechnosphereFlow(name='name', type='Input/Technosphere', unit='unit', amount=4, modification_code=2,
        ...         relevance_code='A', confidence_code='Y', comment='general comment', review_state=2,
        ...         reviewer_comment='Reviewer comment').missing_quality_data)
        ['modification_comment', 'confidence_comment']
        """

        missing_data = []

        if self.modification_code is None:
            missing_data.append('modification_code')

        if self.modification_code != 0 and self.modification_comment is None:
            missing_data.append('modification_comment')

        if self.relevance_code is None:
            missing_data.append('relevance_code')

        if self.relevance_code != 'A' and self.relevance_comment is None:
            missing_data.append('relevance_comment')

        if self.confidence_code is None:
            missing_data.append('confidence_code')

        if self.confidence_comment is None:
            missing_data.append('confidence_comment')

        return missing_data


@dataclass
class BiosphereFlow(Flow):
    """ Class used for modelling of biosphere flows """
    compartment: Optional[str] = None  # Flow compartment
    sub_compartment: Optional[str] = None  # Flow sub_compartment
    relevance_code: Optional[str] = None  # Flow relevance code
    relevance_comment: Optional[str] = None  # Flow relevance comment
    confidence_code: Optional[str] = None  # Numeric value confidence code
    confidence_comment: Optional[str] = None  # Numeric value confidence comment

    def __post_init__(self):
        super().__post_init__()

        if self.type not in BIOSPHERE_FLOW_TYPES:
            raise FlowTypeError(f'{self.type} is not a recognized biosphere flow type.')

    def __repr__(self):
        return super().__repr__()

    def encoded_comment(self, elda_only_data):
        """
        Returns a string containing the comment, quality data, and json encoded data

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Encoded comment

        Examples:
            >>> print(BiosphereFlow(name='name', type='Output/Emission', unit='unit', amount=4,
            ...     relevance_code='A', relevance_comment='relevance comment', confidence_code='Z',
            ...     comment='general comment', review_state=2).encoded_comment(elda_only_data=True))
            AZ:
            A: relevance comment
            Z:
            <BLANKLINE>
            general comment
            <BLANKLINE>
            !!! DO NOT EDIT BELOW THIS LINE !!!
            [[{"review_state": 2}]]
            >>> print(BiosphereFlow(name='name', type='Output/Emission', unit='unit', amount=4,
            ...     relevance_code='A', relevance_comment='relevance comment', confidence_code='Z',
            ...     comment='general comment', review_state=2).encoded_comment(elda_only_data=False))
            AZ:
            A: relevance comment
            Z:
            <BLANKLINE>
            general comment
        """

        return encode_comment('biosphere_flow_comment.jinja2',
                              relevance_code=self.relevance_code,
                              relevance_comment=self.relevance_comment,
                              confidence_code=self.confidence_code,
                              confidence_comment=self.confidence_comment,
                              comment=self.comment,
                              json_data=self.json_data if elda_only_data else None)

    def simapro_csv_format(self, elda_only_data):
        """
        Returns a string formatted for insertion in a SimaPro csv import file.

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Formatted string

        Examples:
            >>> print(BiosphereFlow(name='name2', unit='unit2', type='Output/Emission', compartment='Air',
            ...         sub_compartment='sub-comp', amount=5, review_state=1,
            ...         comment_for_reviewer='Some comment for reviewer', comment='Some comment',
            ...         uncertainty='Lognormal',  stdev=50).simapro_csv_format(elda_only_data=True))
            "name2";"sub-comp";"unit2";5;"Lognormal";50.0;0;0;"Some comment!!! DO NOT EDIT BELOW THIS LINE !!![[{""review_state"": 1, ""comment_for_reviewer"": ""Some comment for reviewer""}]]"
        """

        return encode_simapro_csv_format(self.name, self.sub_compartment or '', self.unit, self.amount,
                                         self.uncertainty or 'Undefined', self.stdev or 0,
                                         self.min_value or 0, self.max_value or 0,
                                         self.encoded_comment(elda_only_data))

    @property
    def missing_quality_data(self):
        """
        Returns the missing quality data of the flow

        Returns:
            list: A list of the missing attributes names

        Examples:
        >>> print(BiosphereFlow(name='name', type='Output/Emission', unit='unit', amount=4,relevance_code='A',
        ...        confidence_code='Y', comment='general comment', review_state=2,
        ...         reviewer_comment='Reviewer comment').missing_quality_data)
        ['confidence_comment']
        """

        missing_data = []

        if self.relevance_code is None:
            missing_data.append('relevance_code')

        if self.relevance_code != 'A' and self.relevance_comment is None:
            missing_data.append('relevance_comment')

        if self.confidence_code is None:
            missing_data.append('confidence_code')

        if self.confidence_comment is None:
            missing_data.append('confidence_comment')

        return missing_data


class Parameter(InventoryData, metaclass=ABCMeta):
    """
    Abstract class describing a parameter of a SimaPro process. Used as parent class by InputParameter and CalculatedParameter
    """

    def __init__(self, name, comment, review_state, comment_for_reviewer, reviewer_comment, level='Process'):
        """
        Args:
            name (str):
            comment (str):
            review_state (int): State of the review (0: No, 1:Yes with changes, 2:Yes)
            comment_for_reviewer (str): Comment for the reviewer
            reviewer_comment (str): Reviewer's comment
            level (str): Process, Project or Database
        """
        self.name = name
        self.comment = comment
        self.review_state = review_state
        self.comment_for_reviewer = comment_for_reviewer
        self.reviewer_comment = reviewer_comment
        self.level = level

    @property
    def json_data(self):
        """
        Returns a json encoded string containing every flow data that are not handled by simapro such as review data.

        Returns:
            str: Json encoded string

        Examples:
            >>> InputParameter(name='name', value=3, review_state=2,
            ...     comment_for_reviewer='Comment for reviewer', reviewer_comment='Reviewer comment').json_data
            '{"review_state": 2, "reviewer_comment": "Reviewer comment", "comment_for_reviewer": "Comment for reviewer"}'
        """

        return encode_json_data(review_state=self.review_state,
                                reviewer_comment=self.reviewer_comment,
                                comment_for_reviewer=self.comment_for_reviewer)

    def encoded_comment(self, elda_only_data):
        """
        Returns a string containing the comment, quality data, and json encoded data

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Encoded comment

        Examples:
            >>> print(InputParameter(name='name', value=5, review_state=1,
            ...         comment_for_reviewer='Some comment for reviewer', comment='Some comment').encoded_comment(elda_only_data=True))
            Some comment
            <BLANKLINE>
            !!! DO NOT EDIT BELOW THIS LINE !!!
            [[{"review_state": 1, "comment_for_reviewer": "Some comment for reviewer"}]]
            >>> print(InputParameter(name='name', value=5, review_state=1,
            ...         comment_for_reviewer='Some comment for reviewer', comment='Some comment').encoded_comment(elda_only_data=False))
            Some comment
        """

        return encode_comment('simple_comment.jinja2',
                              comment=self.comment,
                              json_data=self.json_data if elda_only_data else None)


class InputParameter(Parameter):
    """
    Class describing an user input parameter of a SimaPro Process
    """

    def __init__(self, name, value, comment=None, review_state=0, comment_for_reviewer=None, reviewer_comment=None,
                 uncertainty=None, stdev=None, min_value=None, max_value=None, level='Process'):
        """
        Args:
            name (str):
            value (str or float):
            comment (str):
            review_state (int): State of the review (0: No, 1:Yes with changes, 2:Yes)
            comment_for_reviewer (str): Comment for the reviewer
            reviewer_comment (str): Reviewer's comment
            level (str):
        """
        super().__init__(name=name, comment=comment, review_state=review_state,
                         comment_for_reviewer=comment_for_reviewer, reviewer_comment=reviewer_comment,
                         level=level)
        self.type = 'Input parameter'

        if isinstance(value, str):
            if re.match(r'^=?\d+([.,]\d*)?([eE]-?\d+)?$', value) is not None:
                self.value = float(value.replace(',', '.').replace('=', ''))
            else:
                raise InputParameterValueError(f"Wrong value for input parameter: '{self.name}'\n"
                                               "Input parameters should only have numbers as values.")

        else:
            self.value = value
        self.value_or_formula = self.value

        if uncertainty == 'Undefined':
            self.uncertainty = None
        else:
            self.uncertainty = uncertainty
        self.stdev = n_float(stdev)
        self.min_value = n_float(min_value)
        self.max_value = n_float(max_value)

    def __repr__(self):
        """
        Example:
            >>> str(InputParameter(name='name', comment='comment', value='8,6', level='Process'))
            'name: 8.6'
        """
        return f"{self.name}: {self.value}"

    def __eq__(self, other):
        assert type(other) in (InputParameter, CalculatedParameter)

        if type(other) == CalculatedParameter:
            return False

        return (self.name, self.value, self.comment, self.review_state, self.comment_for_reviewer,
                self.reviewer_comment, self.uncertainty, self.stdev, self.min_value, self.max_value, self.level) == (
                   other.name, other.value, other.comment, other.review_state, other.comment_for_reviewer,
                   other.reviewer_comment, other.uncertainty, other.stdev, other.min_value, other.max_value,
                   other.level)

    def __ne__(self, other):
        return not self.__eq__(other)

    def simapro_csv_format(self, elda_only_data):
        """
        Returns a string formatted for insertion in a SimaPro csv import file.

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Formatted string

        Examples:
            >>> print(InputParameter(name='name', value=3, review_state=2,
            ...     comment_for_reviewer='Comment for reviewer', reviewer_comment='Reviewer comment').simapro_csv_format(elda_only_data=True))
            "name";3;"Undefined";1;0;0;"No";"!!! DO NOT EDIT BELOW THIS LINE !!![[{""review_state"": 2, ""reviewer_comment"": ""Reviewer comment"", ""comment_for_reviewer"": ""Comment for reviewer""}]]"
        """

        return encode_simapro_csv_format(self.name, self.value, self.uncertainty or 'Undefined', self.stdev or 1,
                                         self.min_value or 0, self.max_value or 0, 'No',
                                         self.encoded_comment(elda_only_data))


class CalculatedParameter(Parameter):
    """
    Class describing an user calculated parameter of a SimaPro Process
    """

    def __init__(self, name, formula, comment=None, review_state=0, comment_for_reviewer=None, reviewer_comment=None,
                 level='Process'):
        """
        Args:
            name (str):
            formula (str):
            comment (str):
            review_state (int): State of the review (0: No, 1:Yes with changes, 2:Yes)
            comment_for_reviewer (str): Comment for the reviewer
            reviewer_comment (str): Reviewer's comment
            level (str):
        """
        super().__init__(name=name, comment=comment, review_state=review_state,
                         comment_for_reviewer=comment_for_reviewer, reviewer_comment=reviewer_comment, level=level)
        self.formula = formula
        self.value_or_formula = self.formula
        self.type = 'Calculated parameter'

    def __repr__(self):
        """
        Example:
            >>> str(CalculatedParameter(name='name', comment='comment', formula='A+B', level='Process'))
            'name: A+B'
        """
        return f"{self.name}: {self.formula}"

    def __eq__(self, other):
        assert type(other) in (CalculatedParameter, InputParameter)

        if type(other) == InputParameter:
            return False

        return (self.name, self.formula, self.comment, self.review_state, self.comment_for_reviewer,
                self.reviewer_comment, self.level) == \
               (other.name, other.formula, other.comment, other.review_state, other.comment_for_reviewer,
                other.reviewer_comment, other.level)

    def __ne__(self, other):
        return not self.__eq__(other)

    def simapro_csv_format(self, elda_only_data):
        """
        Returns a string formatted for insertion in a SimaPro csv import file.

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Formatted string

        Examples:
            >>> print(CalculatedParameter(name='name', formula='A+B', review_state=2,
            ...     comment_for_reviewer='Comment for reviewer', reviewer_comment='Reviewer comment').simapro_csv_format(elda_only_data=True))
            "name";"A+B";"!!! DO NOT EDIT BELOW THIS LINE !!!\x7f[[{""review_state"": 2, ""reviewer_comment"": ""Reviewer comment"", ""comment_for_reviewer"": ""Comment for reviewer""}]]"
        """

        return encode_simapro_csv_format(self.name, self.formula, self.encoded_comment(elda_only_data))


@dataclass
class Process(InventoryData):
    """
    Class describing an LCI process
    """

    name: Optional[str] = None  # Process name (optional because SimaPro allows to create processes with no name)
    synonym: Optional[str] = None  # Process synonym
    category_type: Optional[str] = 'Material'
    date: Optional[str] = None  # Process creation date
    comment: Optional[str] = None  # Comment on process
    allocation_rules: Optional[str] = None  # Allocation rules used in the process
    author: Optional[str] = None  # Process author
    contact: Optional[str] = None  # Contact of the process author
    long_term_contact: Optional[str] = None  # Contact of a person ensuring long-term support of the process
    step: Optional[str] = None
    project: Optional[str] = None  # Project the process belongs to
    step_in_project: Optional[str] = None  # Step of the process in this project
    reference_period: Optional[str] = None  # Reference time period for this process
    time_validity_limit: Optional[str] = None
    geographic_representativeness: Optional[str] = None
    technology_description: Optional[str] = None
    technology_scale: Optional[str] = None
    technology_level: Optional[str] = None
    input_mass: Optional[str] = None  # Used for mass balance calculation
    output_mass: Optional[str] = None  # Used for mass balance calculation
    version_creator: Optional[str] = None
    version_contact: Optional[str] = None
    version_comment: Optional[str] = None
    inventory_review_state: Optional[str] = None
    # Dict containing attribute names as keys and dict with review data as values
    metadata_review: Dict[str, dict] = field(default_factory=dict)
    flows: List[Flow] = field(init=False, default_factory=list)
    parameters: List[Parameter] = field(init=False, default_factory=list)

    def __repr__(self):
        return self.name

    @property
    def input_parameters(self):
        """ List of every input parameters related to the process """
        return [parameter for parameter in self.parameters if isinstance(parameter, InputParameter)]

    @property
    def calculated_parameters(self):
        """ List of every calculated parameters related to the process """
        return [parameter for parameter in self.parameters if isinstance(parameter, CalculatedParameter)]

    @property
    def product_flows(self):
        """ List of every product flows related to the process """

        return [flow for flow in self.flows if type(flow) == ProductFlow]

    @property
    def product(self):
        """ Returns the product flow if their is one and only one, None else """
        return self.product_flows[0] if len(self.product_flows) == 1 else None

    @property
    def product_type(self):
        """ Returns the product type (Product or Waste treatment product """
        if self.product_flows == []:
            return None
        else:
            return self.product_flows[0].type

    @property
    def technosphere_flows(self):
        """ List of every technosphere flows related to the process """

        return [flow for flow in self.flows if type(flow) == TechnosphereFlow]

    @property
    def biosphere_flows(self):
        """ List of every biosphere flows related to the process """

        return [flow for flow in self.flows if type(flow) == BiosphereFlow]

    @property
    def json_data(self):
        """
        Returns a json encoded string containing every flow data that are not handled by simapro such as review or
        quality data.

        Returns:
            str: Json encoded string

        Examples:
            >>> Process(name="Process A", synonym="process_a", contact="contact@mail.com").json_data
            '{"synonym": "process_a", "contact": "contact@mail.com"}'
        """

        return encode_json_data(synonym=self.synonym,
                                contact=self.contact,
                                long_term_contact=self.long_term_contact,
                                step=self.step,
                                step_in_project=self.step_in_project,
                                reference_period=self.reference_period,
                                time_validity_limit=self.time_validity_limit,
                                geographic_representativeness=self.geographic_representativeness,
                                technology_description=self.technology_description,
                                technology_scale=self.technology_scale,
                                technology_level=self.technology_level,
                                input_mass=self.input_mass,
                                output_mass=self.output_mass,
                                version_creator=self.version_creator,
                                version_contact=self.version_contact,
                                version_comment=self.version_comment,
                                inventory_review_state=self.inventory_review_state,
                                metadata_review=self.metadata_review or None)

    def encoded_comment(self, elda_only_data):
        """
        Returns a string containing the comment, quality data, and json encoded data

        Args:
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: Encoded comment

        Examples:
            >>> print(Process(name="Process A", synonym="process_a", contact="contact@mail.com",
            ...         comment="Some comment.").encoded_comment(elda_only_data=True))
            Some comment.
            <BLANKLINE>
            !!! DO NOT EDIT BELOW THIS LINE !!!
            [[{"synonym": "process_a", "contact": "contact@mail.com"}]]
            >>> print(Process(name="Process A", synonym="process_a", contact="contact@mail.com",
            ...         comment="Some comment.").encoded_comment(elda_only_data=False))
            Some comment.
        """

        return encode_comment('simple_comment.jinja2',
                              comment=self.comment,
                              json_data=self.json_data if elda_only_data else None)

    def add_flow(self, flow):
        """
        Adds a flow to the process.

        Args:
            flow (Flow): Flow to add
        """

        if type(flow) == ProductFlow:
            if self.product_type == "Output/Technosphere/Waste treatment product":
                raise ProductTypeError(
                    'The process already has a waste treatment product and cannot have another product.')
            elif (self.product_type == "Output/Technosphere/Product") \
                    and (flow.type == "Output/Technosphere/Waste treatment product"):
                raise ProductTypeError(
                    "The process already has product flows and cannot have a waste treatment product flow")

        self.flows.append(flow)

    def add_flows(self, *args):
        """
        Adds mutliple flows at once to the process

        Args:
            *args (Flow): Flows to add
        """

        for flow in args:
            self.add_flow(flow)

    def add_parameter(self, parameter):
        """
        Adds a parameter to the process

        Args:
            parameter (InputParameter or CalculatedParameter): Parameter to add
        """

        self.parameters.append(parameter)

    def add_parameters(self, *args):
        """
        Adds multiple parameters at once to the process

        Args:
            args (InputParameter or CalculatedParameter): Parameters to add
        """
        for parameter in args:
            self.add_parameter(parameter)

    def check_formulas(self):
        """
        Formulas consistency verification and fix.

        Checks if every formula in the process parameters or flows are only using existing parameters names.
        If not, (for exemple if using project or database parameters), creates it as a input parameter of the process.

        Note:
            This method is not used anymore as it is now possible to read Project/Database parameters from the xlsx file.
        """

        flows_formulas = [flow.amount for flow in self.flows if flow.amount_type == "Formula"]
        calculated_parameters_formulas = [parameter.formula for parameter in self.calculated_parameters]

        # Looping on every formula to check it
        for formula in flows_formulas + calculated_parameters_formulas:

            # Parsing the formula
            variables = extract_variables_from_formula(formula)

            # Filtering out numbers
            variables = [variable for variable in variables if
                         re.match('\w+', str(variable)) is not None and re.match('\d+(\.\d*)?', str(variable)) is None]

            # Looping on every variable used in the formula to check if it exists and to create it if not.
            for variable in variables:

                # Checking if the variable exists in SimaPro built-in variables ...
                if variable.lower() in SIMAPRO_BUILT_IN_VARIABLES.keys():
                    continue
                # ... or in process parameters ...
                elif variable in [parameter.name for parameter in self.parameters]:
                    continue
                # ... if not creates the corresponding input parameter
                else:
                    generated_parameter = InputParameter(name=variable,
                                                         comment="Automatically generated parameter",
                                                         value=None,
                                                         level=None)
                    self.add_parameter(generated_parameter)

    def remove_unused_parameters(self):
        """
        Removes unused parameters from the process.

        Note:
            This can be usefull to filter out unused project or database level parameters.
        """

        # Looping as many times as necessary to remove every parameter, even used by unsued parameters.
        while True:
            # Collecting names of every variables used in formulas
            variables = set()

            for flow in self.flows:
                if flow.amount_type == 'Formula':
                    variables |= set(re.split("[ ()+\-/*^=<>]", flow.amount))

            for parameter in self.calculated_parameters:
                variables |= set(re.split("[ ()+\-/*^=<>]", parameter.formula))

            # Removing numeric values and empty strings from variables
            variables = [var.lower() for var in variables if not (re.match('\d+\.?,?\d*', var) or len(var) == 0)]

            # Removing unused parameters
            removed_parameters = [param for param in self.parameters if param.name.lower() not in variables]
            self.parameters = [param for param in self.parameters if param not in removed_parameters]

            # If this cycle didn't delete any parameter, ends the loop.
            if len(removed_parameters) == 0:
                break

    def check_for_missing_parameters(self):
        """
        Checks for parameters used in a formula but absent of the process parameters of SimaPro's built-in variables
        Not case sensitive

        Raises:
            MissingParameterError
        """

        # Collecting names of every variables used in formulas
        variables = set()

        for flow in self.flows:
            if flow.amount_type == 'Formula':
                if re.match(EXCEL_EXTERNAL_LINK_PATTERN, flow.amount) is not None:
                    continue
                variables |= set(re.split("[ ()+\-/*^=<>]", flow.amount))

        for parameter in self.calculated_parameters:
            if re.match(EXCEL_EXTERNAL_LINK_PATTERN, parameter.formula) is not None:
                continue
            variables |= set(re.split("[ ()+\-/*^=<>]", parameter.formula))

        # Removing numeric values and empty string from variables
        variables = [var for var in variables if not (re.match(r'\d+\.?,?\d*', var) or len(var) == 0)]

        # Looking for missing parameter
        missing_parameters = [param for param in variables if param.lower() not in
                              [p.name.lower() for p in self.parameters] + list(SIMAPRO_BUILT_IN_VARIABLES.keys())]

        if len(missing_parameters) == 1:
            raise MissingParameterError(f'1 parameter is missing: {missing_parameters[0]}')
        elif len(missing_parameters) > 1:
            raise MissingParameterError(f"{len(missing_parameters)} parameters are missing: "
                                        f"{', '.join(missing_parameters)}")

    def simapro_csv_format(self, category, elda_only_data=True):
        """
        Returns a simapro csv formatted string containing every data for the given category

        Args:
            category (str): Category of the data to return (as in the simapro csv file)
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment

        Returns:
            str: SimaPro csv formatted string

        Examples:
            >>> flow1 = ProductFlow(name='name', unit='unit', type='Output/Technosphere/Product', review_state=2, amount=5)
            >>> flow2 = ProductFlow(name='name2', unit='unit2', type='Output/Technosphere/Product', amount=5, comment='Some comment')
            >>> process = Process(name='name')
            >>> process.add_flows(flow1, flow2)
            >>> print(process.simapro_csv_format('Products'))
            "name";"unit";5;;"not defined";"ELDAM";"!!! DO NOT EDIT BELOW THIS LINE !!![[{""review_state"": 2}]]"
            "name2";"unit2";5;;"not defined";"ELDAM";"Some comment"
        """

        data = []

        # Getting the category attributes (if a flow)
        flow_category_attr = [cat for cat in FLOW_CATEGORIES if cat[0] == category]

        # Getting the category attributes (if a parameter)
        param_category_attr = [cat for cat in PARAMETER_CATEGORIES if cat[0] == category]

        # If it corresponds to a flow category
        if flow_category_attr:

            flow_category_attr = flow_category_attr[0]
            flow_type = flow_category_attr[2]['Type']
            compartment = flow_category_attr[2].get('Compartment')

            # Gets a list of every corresponding data in SimaPro csv format
            data += [flow.simapro_csv_format(elda_only_data=elda_only_data) for flow in self.flows if
                     flow.type == flow_type and (compartment is None or flow.compartment == compartment)]

        # If it corresponds to a parameter
        elif param_category_attr:

            param_category_attr = param_category_attr[0]
            param_type = param_category_attr[1]['Type']
            level = param_category_attr[1]['Level']

            # Gets a list of every corresponding data in SimaPro csv format
            data += [param.simapro_csv_format(elda_only_data=elda_only_data) for param in self.parameters if
                     param.type == param_type and param.level == level]

        else:
            raise Exception(
                f'Process.simapro_csv_format() has been called with an unexpected category name: {category}')

        return "\n".join(data)

    def sort_parameters(self):
        """ Sorts the process parameters by level (process, database and project) to fit SimaPro's order """
        self.parameters = [param for param in self.parameters if param.level == 'Process'] + \
                          [param for param in self.parameters if param.level == 'Database'] + \
                          [param for param in self.parameters if param.level == 'Project']
