import os


class Generator:
    def __init__(self, report_dir, title=None):
        self._str = ""
        self.report_dir = report_dir
        self.title = title or "Unnamed Report"

    def add_section(self, string):
        self._str += string + "\n\n"

    def print_title(self):
        title_str = f"# {self.title}"
        self.add_section(title_str)

    @staticmethod
    def _str_diff(diff_id, diff):
        diff_str = f"### Difference {diff_id}\n"
        diff_str += f"<img src='{diff.img}' height=150 alt='First image'> was found similar to "
        if diff.conf:
            diff_str += f"<img src='{diff.reference_img}' height=150 alt='First image'> with confidence of {diff.conf}."
        else:
            diff_str += "none :("

        return diff_str

    def print_diffs(self, diff_list):
        diffs_str = "## Similarities Report\n"
        diffs_str += "|Image|Reference|Confidence|\n|---|---|---|\n"
        for i, diff in enumerate(diff_list):
            img1 = f"<img src='{diff.img}' height=150 alt='First image'>"
            img2 = f"<img src='{diff.reference_img if diff.conf else None}' height=150 alt='Second image'>"
            row = f"|{img1}|{img2}|{diff.conf}|\n"
            diffs_str += row
        self.add_section(diffs_str)

    def export(self):
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir, exist_ok=True)
            md_id = 1
        else:
            mds = os.listdir(self.report_dir)
            used_numbers = [md.split(".")[0] for md in mds]
            if used_numbers:
                md_id = int(sorted(used_numbers)[-1]) + 1
            else:
                md_id = 1
        filename = os.path.join(self.report_dir, f"{md_id}.md")
        with open(filename, "w") as f_out:
            f_out.write(self._str)
        print(f"{filename} was exported successfully!")

    def auto(self, diffs):
        self.print_title()
        self.print_diffs(diffs)
        self.export()
