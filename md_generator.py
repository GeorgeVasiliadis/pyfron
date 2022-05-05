class Generator:
    def __init__(self, title):
        self._str = ""
        self.title = title

    def add_section(self, string):
        self._str += string + "\n\n"

    def print_title(self):
        title_str = f"# {self.title}"
        self.add_section(title_str)

    def _str_diff(self, diff_id, diff):
        diff_str = f"### Difference {diff_id}\n"
        diff_str += f"<img src='{diff.img1}' height=150 alt='First image'> was found similar to "
        if diff.conf:
            diff_str += f"<img src='{diff.img2}' height=150 alt='First image'> with confidence of {diff.conf}."
        else:
            diff_str += "none :("

        return diff_str

    def print_diffs(self, diff_list):
        diffs_str = "## All Differences\n"
        for i, diff in enumerate(diff_list):
            diffs_str += self._str_diff(i, diff) + "\n\n"
        self.add_section(diffs_str)

    def export(self):
        filename = f"{self.title}.md"
        with open(filename, "w") as f_out:
            f_out.write(self._str)
        print(f"{filename} was exported successfully!")

    def auto(self, diffs):
        self.print_title()
        self.print_diffs(diffs)
        self.export()
