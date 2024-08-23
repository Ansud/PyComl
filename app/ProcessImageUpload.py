import re
import traceback
from pathlib import Path

from constants import URL
from PyQt6.QtCore import QObject, QTimer, pyqtSlot


class ProcessImageUpload(QObject):
    def __init__(self, element, widget, path, session, index):
        QObject.__init__(self)
        self.element = element
        self.widget = widget
        self.path = path
        self.session = session
        self.index = index

    @pyqtSlot()
    def process(self):
        print("ImageUpload.py-30: process is running")  # noqa: T201
        self.widget.clear_status()
        element = self.element
        path = self.path
        widget = self.widget
        text = self.get_text(element, widget)
        file_name = element.line_edit_file_name.text()
        real_file_name = element.lbl_real_file_name.text()
        file_path = Path(path) / real_file_name
        try:
            # Step 3: Obtain a CSRF token
            query_tokens_params = {"action": "query", "meta": "tokens", "format": "json"}
            http_ret = self.session.get(url=URL, params=query_tokens_params)
            print("ProcessImageUpload-40 http ret (3): " + str(http_ret.json()))  # noqa: T201
            CSRF_TOKEN = http_ret.json()["query"]["tokens"]["csrftoken"]
            # Step 4: Post request to upload a file directly
            if not file_path.is_file():
                element.lbl_upload_result.setText("FAILED")
                self.widget.set_upload_status(False)
                return
            # Manage dot in new filename (according physical file name)
            physical_array = str(file_path).split(".")
            if len(physical_array) > 0:
                physical_ext = physical_array[-1]
                logical_array = file_name.split(".")
                if len(logical_array) > 1:
                    logical_ext = logical_array[-1]
                    if logical_ext != physical_ext:
                        file_name = str(file_name) + "." + str(physical_ext)
                else:
                    file_name = str(file_name) + "." + str(physical_ext)
            else:
                element.lbl_upload_result.setText("FAILED")
                self.widget.set_upload_status(False)
                return
            print("ProcessImageUpload.py-70 logical file name to be sent: " + str(file_name))  # noqa: T201
            params_4 = {
                "action": "upload",
                "filename": file_name,
                "format": "json",
                "token": CSRF_TOKEN,
                "ignorewarnings": 1,
                "comment": "PyCommonist upload: " + file_name,
                "text": text,
            }

            with file_path.open("rb") as f:
                file = {"file": (file_name, f, "multipart/form-data")}
                http_ret = self.session.post(URL, files=file, data=params_4)

            print(str(http_ret))  # noqa: T201
            print("ProcessImageUpload-83 http ret (4): " + str(http_ret.json()))  # noqa: T201
            if "upload" in http_ret.json():
                result_upload_image = http_ret.json()["upload"]["result"]
                element.lbl_upload_result.setText(result_upload_image)
                self.widget.set_upload_status(True)
                element.cb_import.setChecked(False)
            else:  # Second attempt
                element.lbl_upload_result.setText("FAILED")
                self.widget.set_upload_status(False)
                element.cb_import.setChecked(False)
        except Exception:
            traceback.print_exc()
            element.lbl_upload_result.setText("FAILED")
            self.widget.set_upload_status(False)
        self.run_next_thread()

    def run_next_thread(self):
        if self.index < self.widget.number_images_checked - 1:
            timer = QTimer()
            # To avoid a 502 error (first test ok with 10)
            timer.setInterval(6)
            timer.start()
            self.widget.threads[self.index + 1].start()
        elif self.index == self.widget.number_images_checked - 1:
            self.widget.clean_threads()

    def get_text(self, element, widget):
        location = element.lineEditLocation.text()
        if location != "":
            location = location.replace(",", "|")
            location = "{{Location dec|" "" + location + """}}\n"""
        cat_text = widget.line_edit_categories.text() + "|" + element.line_edit_categories.text()
        cat_text = cat_text.replace("| ", "|")
        cat_text = cat_text.replace(" | ", "|")
        cat_text = cat_text.strip()
        if cat_text == "|":
            cat_text = "Uploaded with PyCommonist"
        else:
            cat_text += "|Uploaded with PyCommonist"
        cat_text = cat_text.replace("||", "|")
        print(cat_text)  # noqa: T201
        categories = cat_text.split("|")
        catFinalText = ""
        for category in categories:
            if category:
                # check whether it is a template (starts with {{, ends with }})
                if re.match("^\{\{.*\}\}$", category):
                    catFinalText = catFinalText + category + "\n"
                else:
                    # add brackets ([[Category:category]])
                    catFinalText = catFinalText + "[[Category:" + category + "]]\n"
        description = widget.line_edit_description.toPlainText() + element.line_edit_description.toPlainText()
        language = widget.line_edit_language.text()
        if language:
            description = "{{" + language + "|1=" + description + "}}"

        # additional templates
        additional_templates = element.line_edit_templates.text()
        if additional_templates != "":
            additional_templates = additional_templates + "\n"

        text = (
            """== {{int:filedesc}} ==
{{Information
|Description = """
            + description
            + "\n"
            + """|Source = """
            + widget.line_edit_source.text()
            + "\n"
            + """|Author = """
            + widget.line_edit_author.text()
            + "\n"
            """|Date = """
            + element.line_edit_date_time.text()
            + "\n"
            + """|Permission =
|other versions =
}}\n"""
            + location
            + "\n"
            + additional_templates
            + """== {{int:license-header}} == \n"""
            + widget.line_edit_license.text()
            + "\n\n"
            + catFinalText
        )
        return text
