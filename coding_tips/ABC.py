from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Dict, List, Optional, Sequence, Set, Union


class BaseEngine(ABC):
    r"""
    Base class for inference engine of chat models.

    Must implements async methods: chat(), stream_chat() and get_scores().
    这个函数说明了async相关的类都需要chat,stream_chat 和get_scores这三个函数.
    """

    model: Union["PreTrainedModel", "AsyncLLMEngine"]
    tokenizer: "PreTrainedTokenizer"
    can_generate: bool
    template: "Template"
    generating_args: Dict[str, Any]

    @abstractmethod
    def __init__(
        self,
        model_args: "ModelArguments",
        data_args: "DataArguments",
        finetuning_args: "FinetuningArguments",
        generating_args: "GeneratingArguments",
    ) -> None:
        r"""
        Initializes an inference engine.
        """
        ...

    @abstractmethod
    async def chat(
        self,
        messages: Sequence[Dict[str, str]],
        system: Optional[str] = None,
        tools: Optional[str] = None,
        images: Optional[Sequence["ImageInput"]] = None,
        videos: Optional[Sequence["VideoInput"]] = None,
        **input_kwargs,
    ) -> List["Response"]:
        r"""
        Gets a list of responses of the chat model.
        """
        ...

    @abstractmethod
    async def stream_chat(
        self,
        messages: Sequence[Dict[str, str]],
        system: Optional[str] = None,
        tools: Optional[str] = None,
        images: Optional[Sequence["ImageInput"]] = None,
        videos: Optional[Sequence["VideoInput"]] = None,
        **input_kwargs,
    ) -> AsyncGenerator[str, None]:
        r"""
        Gets the response token-by-token of the chat model.
        """
        ...

    @abstractmethod
    async def get_scores(
        self,
        batch_input: List[str],
        **input_kwargs,
    ) -> List[float]:
        r"""
        Gets a list of scores of the reward model.
        """
        ...


SLOTS = Sequence[Union[str, Set[str], Dict[str, str]]]


@dataclass
class Formatter(ABC):
    slots: SLOTS = field(default_factory=list)
    tool_format: Optional[str] = None

    @abstractmethod
    def apply(self, **kwargs) -> SLOTS:
        r"""
        Forms a list of slots according to the inputs to encode.
        """
        ...

    def extract(self, content: str) -> Union[str, List["FunctionCall"]]:
        r"""
        Extract a list of tuples from the response message if using tools.

        Each tuple consists of function name and function arguments.
        """
        raise NotImplementedError


@dataclass
class StringFormatter(Formatter):
    def __post_init__(self):
        has_placeholder = False
        # filter 可以用来对list里面的元素进行判断并筛选
        for slot in filter(lambda s: isinstance(s, str), self.slots):
            if re.search(r"\{\{[a-zA-Z_][a-zA-Z0-9_]*\}\}", slot):
                has_placeholder = True

        if not has_placeholder:
            raise ValueError("A placeholder is required in the string formatter.")

    @override
    def apply(self, **kwargs) -> SLOTS:
        elements = []
        for slot in self.slots:
            if isinstance(slot, str):
                for name, value in kwargs.items():
                    if not isinstance(value, str):
                        raise RuntimeError(f"Expected a string, got {value}")

                    slot = slot.replace("{{" + name + "}}", value, 1)
                elements.append(slot)
            elif isinstance(slot, (dict, set)):
                elements.append(slot)
            else:
                raise RuntimeError(
                    f"Input must be string, set[str] or dict[str, str], got {type(slot)}"
                )

        return elements
