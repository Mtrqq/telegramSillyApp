import enum
from string import Template
from typing import Type

from pydantic import BaseConfig
from pydantic import BaseModel


class Style(BaseModel):
    fill: str
    empty: str
    prefix: str = "|"
    suffix: str = "|"
    length: int = 10
    percent: bool = True

    template: str = "${prefix}${fill}${suffix} ${percent} ${label}"

    class Config(BaseConfig):
        frozen = True


class PredefinedStyle(enum.Enum):
    CIRCLES = Style(fill="◉", empty="◯")
    CHARGING = Style(fill="█", empty=".")
    SQUARES = Style(fill="▣", empty="▢")
    SIMPLE = Style(fill="+", empty="=")

    @classmethod
    def from_string(cls: Type["PredefinedStyle"], string: str) -> "PredefinedStyle":
        try:
            return cls[string]
        except KeyError:
            raise ValueError(
                f"{string} is not valid member of {cls.__name__}"
            ) from None


def format_percentage(percentage: float) -> str:
    return f"{percentage * 100:.2f}%".rjust(len("100.00%"), " ")


def bar_for(style: Style, current: float, target: float, label: str = "") -> str:
    percentage = current / target
    progress = int(percentage * style.length)
    fill = style.fill * progress
    empty = style.empty * (style.length - progress)

    return Template(style.template).substitute(
        prefix=style.prefix,
        fill=fill + empty,
        suffix=style.suffix,
        percent=format_percentage(percentage) if style.percent else "",
        label=label,
    )
