# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebook_chat.ipynb.

# %% auto 0
__all__ = ['ChatMessages', 'Llama2ChatVersion2']

# %% ../notebook_chat.ipynb 6
class ChatMessages:

    def __init__(self):
        """Initializes the Chat."""
        self._messages = []

    def _append_message(self, role, content):
        """Appends a message with specified role and content to messages list."""
        self._messages.append({"role": role, "content": content})

    def append_system_message(self, content):
        """Appends a system message with specified content to messages list."""
        self._append_message("system", content)

    def append_user_message(self, content):
        """Appends a user message with specified content to messages list."""
        self._append_message("user", content)

    def append_assistant_message(self, content):
        """Appends an assistant message with specified content to messages list."""
        self._append_message("assistant", content)
    
    def get_messages(self):
        """Returns a shallow copy of the messages list."""
        return self._messages[:]

# %% ../notebook_chat.ipynb 8
from IPython.display import Markdown, clear_output

class Llama2ChatVersion2:

    def __init__(self, llm, system_message):
        """Initializes the Chat with the system message."""
        self._llm = llm
        self._chat_messages = ChatMessages()
        self._chat_messages.append_system_message(system_message)

    def _get_llama2_response(self):
        """Returns Llama2 model response for given messages."""
        self.model_response = self._llm.create_chat_completion(self._chat_messages.get_messages())
        return self.model_response['choices'][0]['message']['content']

    def _format_markdown_with_style(self, text, font_size=16):
        """Wraps text in a <span> with specified font size, defaults to 16."""
        return f"<span style='font-size: {font_size}px;'>{text}</span>"

    def prompt_llama2(self, user_prompt):
        """Processes user prompt, displays Llama2 response formatted in Markdown."""
        self._chat_messages.append_user_message(user_prompt)
        llama2_response = self._get_llama2_response()
        self._chat_messages.append_assistant_message(llama2_response)
        display(Markdown(self._format_markdown_with_style(llama2_response)))


    def _get_llama2_response_stream(self):
        """Returns generator object for streaming Llama2 model responses for given messages."""
        return self._llm.create_chat_completion(self._chat_messages.get_messages(), stream=True)

    def prompt_llama2_stream(self, user_prompt):
        """Processes user prompt in streaming mode, displays updates in Markdown."""
        self._chat_messages.append_user_message(user_prompt)
        llama2_response_stream = self._get_llama2_response_stream()
        
        complete_stream = ""

        for part in llama2_response_stream:
            # Check if 'content' key exists in the 'delta' dictionary
            if 'content' in part['choices'][0]['delta']:
                stream_content = part['choices'][0]['delta']['content']
                complete_stream += stream_content
                #self._chat_messages.append_assistant_stream(stream_content)

                # Clear previous output and display new content
                clear_output(wait=True)
                display(Markdown(self._format_markdown_with_style(complete_stream)))

            else:
                # Handle the case where 'content' key is not present
                pass
        
        self._chat_messages.append_assistant_message(complete_stream)