import sys

class SwiftUI:
    def __init__(self):
        self.framework = "SwiftUI"
        self.language = "Swift"
        self.platform = "iOS"

    def describe(self):
        return f"{self.framework} is a UI framework for {self.platform} developed by Apple, using {self.language} programming language."


class JetpackCompose:
    def __init__(self):
        self.framework = "Jetpack Compose"
        self.language = "Kotlin"
        self.platform = "Android"

    def describe(self):
        return f"{self.framework} is a UI framework for {self.platform} developed by Google, using {self.language} programming language."


def main():
    swift_ui = SwiftUI()
    jetpack_compose = JetpackCompose()

    print(swift_ui.describe())
    print(jetpack_compose.describe())


if __name__ == "__main__":
    main()

# NEXUS-ONE CORE MODULE