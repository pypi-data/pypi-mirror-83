from lyrix.lyrics import get_title, get_lyrics, get_name
import tkinter as tk
import json


with open("config.json", "r") as openfile:
    config = json.load(openfile)


class Lyrix:
    def __init__(self, master):
        self.master = master
        self.scope = "user-read-currently-playing"
        self.username = config["username"]
        self.client_id = config["spotify_client_id"]
        self.client_secret = config["spotify_client_secret"]
        self.redirect_uri = "http://localhost:8888/callback/"
        self.client_access_token = config["genius_client_access_token"]
        self.previous_name = ""
        self.name = ""

        self.master.title(
            get_title(
                self.scope,
                self.username,
                self.client_id,
                self.client_secret,
                self.redirect_uri,
            )
        )
        self.text = tk.Text(self.master, wrap="word", font=("PT Sans", "18"))
        self.scroll_y = tk.Scrollbar(
            self.master, orient="vertical", command=self.text.yview
        )

        get_lyrics(
            self.scope,
            self.username,
            self.client_id,
            self.client_secret,
            self.redirect_uri,
            self.client_access_token,
        )
        self.name = get_name(
            self.scope,
            self.username,
            self.client_id,
            self.client_secret,
            self.redirect_uri,
        )

        self.add_lyrics()
        self.new_lyrics()

    def add_lyrics(self):
        self.text.config(state="normal")

        with open("lyrix/lyrics.json", "r") as openfile:
            lyrics = json.load(openfile)["lyrics"]

        self.text.tag_configure("center", justify="center")
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", lyrics)
        self.text.tag_add("center", "1.0", "end")
        self.text.config(state="disabled")
        self.text.pack(side="left", expand=True, fill="both")
        self.scroll_y.pack(side="left", expand=False, fill="y")

        self.text.configure(yscrollcommand=self.scroll_y.set)

    def new_lyrics(self):
        self.master.after(5000, self.new_lyrics)
        self.previous_name = self.name
        self.name = get_name(
            self.scope,
            self.username,
            self.client_id,
            self.client_secret,
            self.redirect_uri,
        )
        if self.name != self.previous_name:
            get_lyrics(
                self.scope,
                self.username,
                self.client_id,
                self.client_secret,
                self.redirect_uri,
                self.client_access_token,
            )

            self.previous_name = self.name

            self.name = get_name(
                self.scope,
                self.username,
                self.client_id,
                self.client_secret,
                self.redirect_uri,
            )

            self.master.title(
                get_title(
                    self.scope,
                    self.username,
                    self.client_id,
                    self.client_secret,
                    self.redirect_uri,
                )
            )

            self.add_lyrics()


def run():
    root = tk.Tk()
    lyrix = Lyrix(root)
    root.mainloop()
