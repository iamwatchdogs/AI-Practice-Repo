"""Project 1: OpenAI Compatible API.

This is the very first project that kickstart the GenAI project
with a simple usage of OpenAI Compatible API sdk provided by OpenAI.

This doesn't necessarily mean that an Actual OpenAI API key will be
use as part of this training/practice.

In this package, we have implement the typed instructions format i.e.,
the LLM request is purely treated as an REST API and not as a mean to
carry out any minimalistic agentic tasks or even have a conversation.

We have create two function: `get_normal_str` and `main`

get_normal_str(str) -> str
    A utility function that converts multi-line string into a single
    line string by removing unnecessary new lines and white spaces.

main(list[Conversation]) -> None
    This the main driver function of the whole project and all the main
    logic is written within this function. The main function only accepts
    list of `Conversation` and the `HARDCODED_CONVERSATIONS` is passed as
    the default argument.

Within this project we have an custom data structure type: `Conversation`

Conversation
    It's a `TypedDict` that helped me spread out the value into the
    `client.responses.create` without having type check issues. This helped
    me set a meaningful type for the `HARDCODED_CONVERSATIONS` and also set
    the expected type of input for the `main` function.
"""
