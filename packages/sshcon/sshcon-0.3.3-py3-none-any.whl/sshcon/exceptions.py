class SshConSftpError(Exception):
    def __init__(self, cmd, rcode):
        self.cmd = cmd
        self.rcode = rcode
        self.message = "Function has failed."
        super().__init__(self.message)

    def __str__(self):
        return f"Function:{self.cmd}, RC:{self.rcode} -> {self.message}"


class SshConError(Exception):
    def __init__(self, function, msg):
        self.function = function
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"Function:{self.function} -> {self.msg}"
