import pytest
from blockkit import (
    Confirm,
    DispatchActionConfig,
    Filter,
    MarkdownText,
    Option,
    OptionGroup,
    PlainText,
    Text,
)
from blockkit.fields import ValidationError


def test_builds_markdown_text(values):
    assert MarkdownText(values.text, verbatim=True).build() == {
        "type": Text.markdown,
        "text": values.text,
        "verbatim": True,
    }


def test_builds_plain_text_with_emoji(values):
    text = PlainText(values.text, emoji=True)
    assert text.build() == {"type": Text.plain, "text": values.text, "emoji": True}


def test_mrkdwn_text_with_emoji_raises_exception(values):
    with pytest.raises(ValidationError):
        Text(values.text, type_=Text.markdown, emoji=True)


def test_plain_text_with_verbatim_raises_exception(values):
    with pytest.raises(ValidationError):
        Text(values.text, type_=Text.plain, verbatim=True)


def test_builds_confirm(plain_text, markdown_text, values):
    confirm = Confirm(
        plain_text,
        markdown_text,
        Text(values.confirm_text, type_=Text.plain),
        Text(values.deny_text, type_=Text.plain),
    )

    assert confirm.build() == {
        "title": {"type": Text.plain, "text": values.text},
        "text": {"type": Text.markdown, "text": values.text},
        "confirm": {"type": Text.plain, "text": values.confirm_text},
        "deny": {"type": Text.plain, "text": values.deny_text},
    }


def test_builds_option(plain_text, values):
    option = Option(plain_text, values.value, values.url, plain_text)

    assert option.build() == {
        "text": {"type": Text.plain, "text": values.text},
        "value": values.value,
        "url": values.url,
        "description": {"type": Text.plain, "text": values.text},
    }


def test_builds_option_group(plain_text, option, values):
    option_group = OptionGroup(plain_text, [option for _ in range(3)])

    assert option_group.build() == {
        "label": {"type": Text.plain, "text": values.text},
        "options": [option.build() for _ in range(3)],
    }


def test_builds_filter():
    include = ["im", "mpim", "private", "public"]

    filter_ = Filter(
        include=include,
        exclude_external_shared_channels=False,
        exclude_bot_users=False,
    )

    assert filter_.build() == {
        "include": include,
        "exclude_external_shared_channels": False,
        "exclude_bot_users": False,
    }


def test_filter_without_args_raises_exception():
    with pytest.raises(ValidationError):
        Filter()


def test_filter_with_incorrect_include_raises_exception():
    with pytest.raises(ValidationError):
        Filter(include=["group"])


def test_builds_dispatch_action_config():
    triggers = ["on_enter_pressed", "on_character_entered"]
    config = DispatchActionConfig(trigger_actions_on=triggers)

    assert config.build() == {"trigger_actions_on": triggers}


def test_dispatch_action_config_raises_exception_on_incorrect_triggers():
    with pytest.raises(ValidationError):
        DispatchActionConfig(trigger_actions_on=["on_something_happened"])


def test_dispatch_action_config_raises_exception_on_empty_triggers():
    with pytest.raises(ValidationError):
        DispatchActionConfig(trigger_actions_on=[])


def test_dispatch_action_config_raises_exception_on_too_many_triggers():
    with pytest.raises(ValidationError):
        DispatchActionConfig(
            trigger_actions_on=[
                "on_enter_pressed",
                "on_enter_pressed",
                "on_enter_pressed",
            ]
        )
