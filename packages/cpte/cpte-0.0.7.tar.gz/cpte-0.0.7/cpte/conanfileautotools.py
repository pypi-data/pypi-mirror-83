from conans import AutoToolsBuildEnvironment, tools
from .conanfilemeson import ConanFileMeson


class ConanFileAutoTools(ConanFileMeson):
    _autogen_command = 'NOCONFIGURE=1 ./autogen.sh'

    def _configure_builder(self):
        if self._builder:
            return self._builder

        args = self._args or []

        if self.options.shared:
            args.extend(['--disable-static', '--enable-shared'])
        else:
            args.extend(['--disable-shared', '--enable-static'])

        self._builder = AutoToolsBuildEnvironment(self)
        self.run(self._autogen_command)
        self._builder.configure(args=args)

        return self._builder

    def build(self):
        builder = self._configure_builder()
        builder.make()
