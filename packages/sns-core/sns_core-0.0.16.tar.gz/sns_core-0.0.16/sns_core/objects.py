from .exceptions import SNSobjectException

class SNSinteraction:

    def __init__(self, type, action, headers={}, content=None):
        self.type = str(type)
        self.action = str(action)
        self.headers = headers
        self.content = SNScontent(content)

    def get(self, key, default=None):
        return self.headers.get(key, default)

    def copy(self):
        new_interaction = SNSinteraction(self.type, self.action, self.headers.copy(), self.content.copy())
        return new_interaction

    def __str__(self):
        interaction_string = self.type + " " + self.action

        if len(self.headers) > 0:
            interaction_string += '\r\n'
            interaction_string += '\r\n'.join([header[0] + ": " + str(header[1]) for header in self.headers.items()])

        interaction_string += '\r\n\r\n'

        content_string = str(self.content)

        if len(content_string) > 0:
            return interaction_string + content_string
        else:
            return interaction_string

class SNScontent:

    def __init__(self, content=None):
        self.content = {}

        self.append(content)

    def append_list(self, content):
        for item in content:
            self.append(item)

    def append(self, content):
        if type(content) == str:
            # try to parse, since it's probably decrypted content
            content_parameters = content.splitlines()

            for content_parameter in content_parameters:
                if content_parameter.count(': ') < 1:
                    raise SNSobjectException(content, "Content was passed as a str, but could not be parsed to a dict")

                param_type, param_value = content_parameter.split(': ', 1)

                if param_type not in self.content:
                    self.content[param_type] = param_value
                else:
                    raise SNSobjectException(content, 'One parameter is already given and therefore this SNScontent cannot be parsed')
        elif isinstance(content, dict):
            # decrypted content
            for key, value in content.items():
                if key not in self.content:
                    self.content[key] = value
                else:
                    raise SNSobjectException(content, 'One parameter is already given and therefore this SNScontent cannot be parsed')
        elif type(content) == bytes:
            # could be encrypted content, by parsing we can find out
            try:
                self.append(content.decode('utf-8'))
            except:
                raise SNSobjectException(content, "Tried converted byte array to str, but this could not be done")
        elif type(content) == SNScontent:
            # somehow we got an SNScontent object, just unpack and add to this class
            self.append(content.content)
        elif isinstance(content, list):
            self.append_list(content)

    def get(self, key, default=None):
        return self.content.get(key, default)

    def length(self):
        return len(self.content)

    def copy(self):
        new_content = SNScontent(self.content.copy())
        return new_content

    def __len__(self):
        return len(self.content)

    def __getitem__(self, key):
        return self.content[key]

    def __str__(self):
        return '\r\n'.join([key + ": " + value for key, value in self.content.items()]) + '\r\n\r\n'