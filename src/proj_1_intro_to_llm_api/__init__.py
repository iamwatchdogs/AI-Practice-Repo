"""Project 1: Intro to LLM API.

This is the very first project that kickstart the GenAI project
with a simple usage of OpenAI Compatible API sdk provided by OpenAI.

This doesn't necessarily mean that an Actual OpenAI API key will be
use as part of this training/practice. This will be clarified in future
projects

In this package, we have implement the typed instructions format i.e.,
the LLM request is purely treated as an REST API and not as a mean to
carry out any minimalistic agentic tasks or even have a conversation.

Within this project, we have following functions:

main() -> None
    This the main driver function of the whole project and all the main
    logic is written within this function. The main function loads all the
    conversations from an extneral json file and perform the API call to the
    LLM via OpenAI API Client.

Within this project we have an custom data structure type: `Conversation`

Conversation
    It's a `TypedDict` that helped me spread out the value into the
    `client.responses.create` without having type check issues. This helped
    me set a meaningful type for the `HARDCODED_CONVERSATIONS` and also set
    the expected type of input for the `main` function.
"""
