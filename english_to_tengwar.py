#!/usr/bin/env python3
"""
This file converts English text to Tengwar or Black Speech, using personal preferences for
transliterating Tengwar (as extracted from the Tengwar Textbook) and Black Speech mappings.

Currently, the output that is created is intended for use with the Tengwar Annatar font
and related font families.

Example usage:
    >>> from english_to_tengwar import convert_tengwar, convert_black_speech
    >>> convert_tengwar("This was a triumph. I'm making a note here: huge success!")
    >>> convert_black_speech("One Ring to rule them all")

-- then paste the resulting text into a document rendered in Tengwar Annatar.

To run unit tests on this file:
$ python -m unittest english_to_tengwar

Special characters: T for theta, D for eth
R for pre-vowel r, S and Z for vowel-less s and z
Q for rd, L for ld, W for wh, C for ch, K for kh, G for gh, X for sh, H for
zh, N for ng
"""

import re
from typing import Dict
from unittest import TestCase
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import pyperclip


# Black Speech word mappings
black_speech_dictionary = {
    # Core Ring inscription words
    "one": "ash",
    "ring": "nazg",
    "to": "",  # Often omitted or implied
    "rule": "gimbatul",
    "them": "agh",
    "all": "burzum-ishi",
    "and": "agh",
    "in": "",  # Often implied
    "the": "",  # Often omitted
    "of": "",  # Often omitted or implied in Black Speech
    "darkness": "burzum",
    "bind": "krimpatul",
    
    # Basic vocabulary
    "lord": "uzbad",
    "master": "uzbad",
    "king": "uzbad",
    "fire": "gabil",
    "flame": "gabil",
    "shadow": "glob",
    "dark": "burzum",
    "black": "morn",
    "death": "gûl",
    "evil": "gûl",
    "mountain": "gundu",
    "tower": "barad",
    "fortress": "barad",
    "iron": "ang",
    "steel": "ang",
    "sword": "gurth",
    "blade": "gurth",
    "hand": "gabil",
    "eye": "lugburz",
    "power": "gash",
    "strength": "gash",
    "great": "uruk",
    "mighty": "uruk",
    "servant": "olog",
    "slave": "snaga",
    "come": "gû",
    "go": "gû",
    "bring": "thurkh",
    "take": "thurkh",
    "kill": "agh",
    "destroy": "agh",
    "burn": "gabil",
    "break": "krith",
    "mine": "khaz",
    "gold": "khaz",
    "treasure": "khaz",
    "doom": "dûm",
    "fate": "dûm",
    "war": "gabil",
    "battle": "gabil",
    "blood": "gû",
    "pain": "gash",
    "fear": "gûl",
    "terror": "gûl",
    "hate": "goth",
    "anger": "goth",
    "wrath": "goth",
    "sorrow": "nuin",
    "grief": "nuin",
    "stone": "khaz",
    "earth": "khaz",
    "ground": "khaz",
    "sky": "menel",
    "star": "gil",
    "moon": "ithil",
    "sun": "anor",
    "light": "gal",
    "water": "nen",
    "river": "nen",
    "sea": "gaer",
    "wind": "gwaih",
    "storm": "gwaih",
    "thunder": "gabil",
    "lightning": "gabil",
    "cold": "ring",
    "ice": "ring",
    "snow": "ring",
    "hot": "gabil",
    "warm": "gabil",
    "big": "uruk",
    "large": "uruk",
    "huge": "uruk",
    "small": "snaga",
    "little": "snaga",
    "tiny": "snaga",
    "good": "gâl",  # Ironically used
    "bad": "gûl",
    "beautiful": "gâl",  # Sarcastically
    "ugly": "goth",
    "strong": "gash",
    "weak": "snaga",
    "fast": "thurkh",
    "slow": "glob",
    "high": "barad",
    "low": "glob",
    "far": "ungol",
    "near": "gû",
    "old": "iaur",
    "new": "shin",
    "young": "shin",
    "dead": "gûl",
    "alive": "cuio",
    "born": "no",
    "die": "gûl",
    "live": "cuio",
    "eat": "gor",
    "drink": "sûl",
    "sleep": "lûth",
    "wake": "daw",
    "speak": "lam",
    "hear": "lasta",
    "see": "tîr",
    "know": "ista",
    "think": "saed",
    "remember": "min",
    "forget": "delu",
    "love": "mel",  # Twisted meaning
    "like": "mel",
    "want": "min",
    "need": "bane",
    "have": "har",
    "give": "anno",
    "receive": "goth",
    "find": "hir",
    "lose": "delu",
    "win": "tuv",
    "lose": "delu",
    "begin": "edra",
    "end": "teith",
    "stop": "dar",
    "continue": "minno",
    "change": "wend",
    "stay": "dar",
    "move": "minno",
    "run": "thurkh",
    "walk": "minno",
    "fly": "gwaih",
    "fall": "dant",
    "rise": "orch",
    "climb": "orch",
    "jump": "cab",
    "swim": "luin",
    "work": "bane",
    "rest": "lûth",
    "play": "telu",  # Mockingly
    "fight": "gabil",
    "attack": "dagr",
    "defend": "thang",
    "escape": "rhosg",
    "hide": "thurin",
    "show": "tol",
    "open": "edra",
    "close": "thar",
    "build": "thang",
    "destroy": "agh",
    "create": "caro",
    "make": "caro",
    "repair": "aeg",
    "break": "krith",
    "cut": "risk",
    "join": "gwedh",
    "separate": "palan",
    "mix": "gwaed",
    "clean": "glan",
    "dirty": "goth",
    "wash": "luin",
    "wear": "gwann",
    "remove": "eitha",
    "put": "gwaed",
    "place": "gwaed",
    "turn": "hwinion",
    "push": "thaur",
    "pull": "gwedh",
    "lift": "orgon",
    "drop": "dant",
    "throw": "hab",
    "catch": "rap",
    "hold": "gabil",
    "release": "leithia",
    "touch": "lav",
    "hit": "dagr",
    "kick": "dag",
    "bite": "nasg",
    "scratch": "rasc",
    "burn": "gabil",
    "freeze": "ring",
    "melt": "thaw",
    "boil": "gabil",
    "cook": "gabil",
    "raw": "glass",
    "ripe": "beren",
    "rotten": "goth",
    "sharp": "maeg",
    "dull": "thind",
    "smooth": "balan",
    "rough": "gaern",
    "hard": "sarn",
    "soft": "lind",
    "heavy": "luin",
    "light": "gal",
    "thick": "tiugh",
    "thin": "nim",
    "wide": "palan",
    "narrow": "aeg",
    "deep": "nunn",
    "shallow": "taw",
    "empty": "lhaw",
    "full": "bell",
    "wet": "nîn",
    "dry": "rû",
    "clean": "glan",
    "dirty": "gorth"
}

# Black Speech phonetic patterns - harsher, more guttural sounds
black_speech_phonetics = {
    'c': 'k',  # Always hard K sound
    'soft_g': 'gh',  # G before e,i,y becomes GH
    'th': 'thr',  # TH becomes THR
    'ph': 'f',
    'ch': 'kh',  # CH becomes KH
    'sh': 'shr',  # SH becomes SHR
    'j': 'zh',  # J becomes ZH
    'qu': 'kw',
    'x': 'ks',
    'tion': 'zhon',
    'sion': 'zhon'
}


def dictzip(str1: str, str2: str) -> Dict[str, str]:
    output = {}
    assert len(str1) == len(str2)

    for i in range(len(str1)):
        output[str1[i]] = str2[i]

    return output


def convert_to_black_speech(inp: str) -> str:
    """Convert English text to Black Speech"""
    if not inp.strip():
        return inp
        
    # Split into words and punctuation
    tokens = re.findall(r'\b\w+\b|[^\w\s]', inp.lower())
    result = []
    
    for token in tokens:
        if token.isalpha():
            # Check for direct word mapping first
            if token in black_speech_dictionary:
                black_word = black_speech_dictionary[token]
                if black_word:  # Skip empty mappings (like "the", "to")
                    result.append(black_word)
            else:
                # Apply phonetic transformations for unknown words
                transformed = apply_black_speech_phonetics(token)
                result.append(transformed)
        else:
            # Keep punctuation as-is
            result.append(token)
    
    return ' '.join(result)


def apply_black_speech_phonetics(word: str) -> str:
    """Apply Black Speech phonetic rules to make words sound more harsh/guttural"""
    # Apply multi-character replacements first
    for pattern, replacement in black_speech_phonetics.items():
        if pattern in word:
            if pattern == 'soft_g':
                # Handle soft G (before e, i, y)
                word = re.sub(r'g(?=[eiy])', 'gh', word)
            else:
                word = word.replace(pattern, replacement)
    
    # Additional harsh transformations
    word = word.replace('v', 'f')  # V becomes F
    word = word.replace('w', 'v')  # W becomes V 
    word = word.replace('y', 'i')  # Y becomes I
    word = re.sub(r'([aeiou])\1', r'\1', word)  # Reduce double vowels
    word = re.sub(r's$', 'z', word)  # Final S becomes Z
    word = re.sub(r'ed$', 'ad', word)  # -ed becomes -ad
    word = re.sub(r'ing$', 'ugh', word)  # -ing becomes -ugh
    
    # Add guttural emphasis to certain patterns
    word = word.replace('oo', 'û')
    word = word.replace('ee', 'î')
    word = word.replace('aa', 'â')
    
    return word


# So, English has two different pronunciations of 'th', and Tengwar distinguishes
# between them. TODO: use a library to determine which 'th' we're dealing with. In the
# meantime: voiced 'th' is the rare one, so these cases handle that.

# replace only the first instance of th
voiced_th_prefices = [
    "their",
    "these",
    "those",
    "although",
    "them",
    "thine",
    "thy",
    "thou",
    "there",
]

# replace only the second instance of th
voiced_th_special_prefices = ["thither"]

# must be alone -- punctuation may extend them, but consider 'thank' -- these aren't
# prefixes
voiced_th_solo_prefices = ["that", "this", "than", "they", "thee", "though"]

# should have only one th apiece
voiced_th_always_safe = [
    "feather",
    "together",
    "bathing",
    "bathe",
    "father",
    "mother",
    "clothing",
    "clothe",
    "brother",
    "weather",
    "either",
    "gather",
    "other",
    "another",
    "worthy",
    "rather",
    "soothing",
    "soothe",
    "smooth",
    "leather",
    "tether",
    "breathe",
    "breathing",
    "lathe",
    "seethe",
    "seething",
    "scathe",
    "scathing",
    "teethe",
    "teething",
    "loath",
    "loathing",
    "neither",
    "thence",
    "rhythm",
    "slither",
    "southern",
    "bother",
    "altogether",
    "lather",
    "hither",
]


def replace_th(inp):
    for x in voiced_th_always_safe:
        if x in inp:
            inp = inp.replace(x, x.replace("th", "TH"))
    for x in voiced_th_solo_prefices:
        if x == inp:
            inp = inp.replace("th", "TH")
    for x in voiced_th_prefices:
        if inp[: len(x)] == x:
            inp = inp.replace(x, x.replace("th", "TH"))
    for x in voiced_th_special_prefices:
        if inp[: len(x)] == x:
            inp = inp.replace(x, x.replace("th", "TH", 2).replace("TH", "th", 1))
    return inp


punctuation = {
    ".": "-",
    ",": "\xb7",
    "!": "\xc1",
    "?": "\xc0",
    ";": "\xc3",
    '"': "\xbb",
    "'": "\xb2",
    "_": "·",
    "-": "·",
    "`": "\xb1",
    ":": "-",
    "/": "\u203a",
    "\\": "\u203a",
    "<": "Œ",
    ">": "œ",
    "[": "Œ",
    "]": "œ",
    "{": "Œ",
    "}": "œ",
    "(": "Œ",
    ")": "œ",
    "@": "1E",
    "#": "9dE1x#",
    "$": "k\xa1",
    "%": "q6R85$1",
    "^": "z7D1R",
    "&": "5#2",
    "*": "\u02c6",
    "=": "\xac",
    "+": "` \xb0",
    "|": "\xbd",
    " ": " ",
    "\n": "\n",
    "\t": "\xb7-\xb7",
}


def tengwar_start(inp) -> str:
    split_inp = re.findall(
        r"[^\W_]+|[.,!\?;\"'-_`:<>/\\\[\]\(\){}@#$%^&\*=\+| \n]", inp
    )
    output = ""
    for item in split_inp:
        output += tengwar_token(item)

    return output


def tengwar_token(item):
    if item in punctuation.keys():
        return punctuation[item]
    if item.isdigit():
        return tengwar_number(int(item))
    item = item.replace("'", "")
    return tengwar_word(item)


def tengwar_number(num: int) -> str:
    # TODO: implement fancy base-12 Elvish numerals
    return "`````"


def tengwar_word(inp) -> str:
    inp = inp.lower()

    if inp == "":
        return inp

    # Detect 'of'
    if inp == "of":
        return "W"

    # Detect 'the'
    if inp == "the":
        return "@"

    # Detect voiced th, replace with TH
    inp = replace_th(inp)

    # Detect hard and soft c and g
    for i in range(len(inp) - 1):
        first = inp[:i]
        cur = inp[i]
        rest = inp[i + 1 :]
        if cur == "g":
            if rest[0] in "eiy":
                inp = first + "j" + rest
        elif cur == "c":
            if rest[0] in "eiy":
                inp = first + "s" + rest
            elif rest[0] in "h":
                inp = first + "C" + rest  # Ch
            else:
                inp = first + "k" + rest
    if inp[-1] == "c":
        inp = inp[:-1] + "k"

    # Detect places where we can use the pre-vowel r
    for i in range(len(inp) - 1):
        if inp[i] == "r" and inp[i + 1] in "aeiouy":
            inp = inp[:i] + "R" + inp[i + 1 :]

    # q == k
    inp = inp.replace("q", "k")

    # Detect differences between consonant y (henceforth Y) and vowel y
    # All ys which do not come before a vowel are consonants
    # Hey, it's just like r!
    for i in range(len(inp) - 1):
        if inp[i] == "y" and inp[i + 1] in "aeiou":
            inp = inp[:i] + "Y" + inp[i + 1 :]

    # Detach the ending s if we notice one... and it's not after aiou
    if len(inp) > 0 and inp[-1] == "s":
        if len(inp) > 1 and inp[-2] not in "aiou":
            inp = inp[:-1]
            has_trailing_s = True
        else:
            has_trailing_s = False
    else:
        has_trailing_s = False

    # Detach the ending e if we notice one -- note, it must be:
    # vowel THEN consonant THEN e
    if len(inp) >= 3 and inp[-1] == "e" and inp[-2] not in "aeiouy":
        inp = inp[:-1]
        has_trailing_e = True
    else:
        has_trailing_e = False

    # Elfification
    if len(inp) == 0:
        output = carrier
    else:
        output = tengwar_postfix(inp)

    # Detect places where we can use the not-post-vowel s and z
    for i in range(len(output) - 1):
        # fancy S
        if output[i] == "i" and output[i + 1] not in vowels:
            output = output[:i] + "8" + output[i + 1 :]
        # fancy Z
        if output[i] == "," and output[i + 1] not in vowels:
            output = output[:i] + "k" + output[i + 1 :]

    # Add the ending e if we detached it earlier
    if has_trailing_e:
        output = output + "O"

    # Add the ending s if we detached it earlier
    if has_trailing_s:
        if output[-1] in "7um8k":
            output = output + "\xc5"
        elif output[-1] in "qwertyo":
            output = output + "\xc6"
        elif output[-1] in "l9":
            output = output + "\xa5"
        else:
            output = output + "_"

    return output


consonants = dictzip("tdnrRhpbfvmwsj--lYkg-z-", "125679qwertyisghjlzxn,.")

doubles = {
    "sh": "d",
    "zh": "f",
    "ch": "a",
    "Ch": "a",
    "ph": "e",
    "kh": "c",
    "gh": "v",
    "wh": "o",
    "ng": "b",
    "rd": "u",
    "ld": "m",
    "th": "3",
    "TH": "4",  # voiced
}

vowel_series = {
    "a": "#EDC",
    "e": "$RFV",
    "i": "%TGB",
    "o": "^YHN",
    "u": "&UJM",
    "y": "\xd8\xd9\xda\xdb",
}

vowels = "#EDC$RFV%TGB^YHN&UJM"

# Index into the output of vowel_series.
# For example, a 0 before an A yields #.
vowels_for_consonants = {
    "`": 3,
    "~": 3,
    "1": 1,
    "q": 1,
    "a": 2,
    "z": 2,
    "2": 0,
    "w": 0,
    "s": 0,
    "x": 0,
    "3": 2,
    "e": 2,
    "d": 1,
    "c": 1,
    "4": 0,
    "r": 0,
    "f": 0,
    "v": 0,
    "5": 0,
    "t": 0,
    "g": 0,
    "b": 0,
    "6": 1,
    "y": 1,
    "h": 2,
    "n": 2,
    "7": 2,
    "u": 2,
    "j": 0,
    "m": 0,
    "i": 2,
    ",": 2,
    "9": 3,
    "o": 0,
    "l": 2,
    ".": 2,
}

short_carrier = "`"
carrier = short_carrier
long_carrier = "~"


def tengwar_postfix(postfix):
    if len(postfix) == 0:
        return ""

    # TODO: Actually add the appropriate character
    if not postfix[0].isalpha():
        return "`" + tengwar_postfix(postfix[1:])

    # Check whether we can apply a double -- if so, apply and recurse
    for double in doubles:
        if postfix[: len(double)] == double:
            return doubles[double] + tengwar_postfix(postfix[len(double) :])

    # Otherwise, apply the appropriate consonant or vowel placeholder
    nxt = postfix[0]
    postfix = postfix[1:]

    # If it's a vowel: Check whether the next thing == a vowel; if so, add the carrier.
    # If not, add the appropriate vowel for the consonant that's coming next.
    # This requires that we first recurse, then check!
    if nxt in vowel_series.keys():
        if len(postfix) == 0:
            next_consonant = carrier  # add a carrier -- we're at the end of the word
        elif postfix[0] in vowel_series.keys():
            next_consonant = carrier  # add a carrier -- the next thing == a vowel
        else:
            rest = tengwar_postfix(postfix)
            next_consonant = rest[0]
            vowel_to_add = vowel_series[nxt][vowels_for_consonants[next_consonant]]
            return next_consonant + vowel_to_add + rest[1:]

        vowel_to_add = vowel_series[nxt][vowels_for_consonants[next_consonant]]
        return next_consonant + vowel_to_add + tengwar_postfix(postfix)

    # If it's a consonant, add it!
    # TODO: Maybe add a doubler ('") if the next consonant == the same thing!
    if nxt in consonants.keys():
        next_consonant = consonants[nxt]
        return next_consonant + tengwar_postfix(postfix)

    if nxt == "x":
        return "z\xe6" + tengwar_postfix(postfix)

    # Otherwise, raise an error!
    else:
        raise NotImplementedError("%s, %s" % (nxt, postfix))

    # TODO: Fancy n-bars and w-bars here.
    return postfix


# Legacy function names for backward compatibility
convert = tengwar_start
convert_tengwar = tengwar_start
convert_black_speech = convert_to_black_speech


class TengwarGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("English to Tengwar & Black Speech Converter")
        self.root.geometry("700x600")
        
        # Mode selection
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="Conversion Mode:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="tengwar")
        ttk.Radiobutton(mode_frame, text="Tengwar Script", variable=self.mode_var, 
                       value="tengwar", command=self.update_mode).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Black Speech", variable=self.mode_var, 
                       value="black_speech", command=self.update_mode).pack(side=tk.LEFT, padx=10)
        
        # Input section
        tk.Label(self.root, text="Enter English text:", font=("Arial", 12, "bold")).pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(self.root, height=6, width=80, font=("Arial", 10))
        self.input_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.convert_button = tk.Button(button_frame, text="Convert to Tengwar", command=self.convert_text, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20)
        self.convert_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Clear", command=self.clear_text, 
                 bg="#f44336", fg="white", font=("Arial", 10), padx=20).pack(side=tk.LEFT, padx=5)
        
        self.copy_button = tk.Button(button_frame, text="Copy Result", command=self.copy_result, 
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=20)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        # Output section
        self.output_label = tk.Label(self.root, text="Tengwar output (use with Tengwar Annatar font):", 
                font=("Arial", 12, "bold"))
        self.output_label.pack(pady=(20,5))
        
        self.output_text = scrolledtext.ScrolledText(self.root, height=6, width=80, 
                                                   font=("Tengwar Annatar", 14), state=tk.DISABLED)
        self.output_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Instructions
        self.instructions_label = tk.Label(self.root, justify=tk.LEFT, font=("Arial", 8), fg="gray")
        self.instructions_label.pack(pady=5, padx=10, anchor='w')
        
        # Initialize mode
        self.update_mode()
    
    def update_mode(self):
        """Update GUI elements based on selected mode"""
        mode = self.mode_var.get()
        
        if mode == "tengwar":
            self.convert_button.config(text="Convert to Tengwar")
            self.copy_button.config(text="Copy Tengwar")
            self.output_label.config(text="Tengwar output (use with Tengwar Annatar font):")
            self.output_text.config(font=("Tengwar Annatar", 14))
            instructions = ("Tengwar Mode Instructions:\n"
                          "1. Type English text in the input box\n"
                          "2. Click 'Convert to Tengwar' to translate to Tengwar script\n"
                          "3. Use 'Copy Tengwar' to copy the result to clipboard\n"
                          "4. Paste into a document with Tengwar Annatar font for proper display")
        else:  # black_speech
            self.convert_button.config(text="Convert to Black Speech")
            self.copy_button.config(text="Copy Black Speech")
            self.output_label.config(text="Black Speech output:")
            self.output_text.config(font=("Arial", 12))
            instructions = ("Black Speech Mode Instructions:\n"
                          "1. Type English text in the input box\n"
                          "2. Click 'Convert to Black Speech' to translate\n"
                          "3. Use 'Copy Black Speech' to copy the result to clipboard\n"
                          "4. Known words are translated directly, unknown words are phonetically adapted")
        
        self.instructions_label.config(text=instructions)
    
    def convert_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if input_text:
            try:
                mode = self.mode_var.get()
                if mode == "tengwar":
                    result = convert_tengwar(input_text)
                else:  # black_speech
                    result = convert_black_speech(input_text)
                
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", result)
                self.output_text.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter some text to convert!")
    
    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def copy_result(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            try:
                pyperclip.copy(result)
                mode_name = "Tengwar" if self.mode_var.get() == "tengwar" else "Black Speech"
                messagebox.showinfo("Copied", f"{mode_name} text copied to clipboard!")
            except:
                # Fallback if pyperclip not available
                self.root.clipboard_clear()
                self.root.clipboard_append(result)
                mode_name = "Tengwar" if self.mode_var.get() == "tengwar" else "Black Speech"
                messagebox.showinfo("Copied", f"{mode_name} text copied to clipboard!")
        else:
            mode_name = "Tengwar" if self.mode_var.get() == "tengwar" else "Black Speech"
            messagebox.showwarning("Warning", f"No {mode_name} text to copy!")
    
    def run(self):
        self.root.mainloop()


def run_gui():
    """Launch the GUI application"""
    app = TengwarGUI()
    app.run()


class TengwarTest(TestCase):
    maxDiff = 10000

    def test_noop(self):
        for pair in blog_post_for_unittest.split("\n\n"):
            first, second = pair.strip().split("\n")
            expected = second.strip()
            actual = convert(first).strip().replace("  ", " ")
            self.assertEqual(expected, actual)


blog_post_for_unittest = r"""
Transliterating Tengwar
175#8j1T7F1Eb% 1b$y6E

Tengwar is a writing system invented by J.R.R. Tolkien for use by the elves of Middle-Earth. Lately, I’ve learned how to write in Tengwar – not by learning any Elvish language, but by learning how to transliterate English into Tengwar using the instructions found in the Tengwar Textbook.
1b$y6E iG `C y71Tb% 88Ú1t$ 5%r5$12$ w`Û s-6-6- 1j^z`B5$ e6Y iJO w`Û @ j$rO_ W t2%2jO·`V6E3- j1Ej$`Û· `Br`V j`V6E52$ 9yY 1`N y71TO 5% 1b$y6E 51Y w`Û j`V6E5b% 5#`Û j$rdT jb#`Ms#O· w1U w`Û j`V6E5b% 9yY 1`N 175#8j1T7F1EO b$jdT 5%1`N 1b$y6E iJb% @ 5%817zJ1`B5^_ e`N5&2 5% @ 1b$y6E 1zFæ1w`NzH-

I’ve found this writing system to be useful for writing down small notes-to-self, and I’ve become quite good at writing it.
`Br`V e`N5&2 4iG y71Tb% 88Ú1t$ 1`N w`V iJeFj& e6Y y71Tb% 2yY5 8tj#j 51YO_·1`N·8j$e· 5#2 `Br`V wzFt^O z`M1TO x`N2^ 1E y71Tb% 1T-

Problem is, I’m still no good at reading Tengwar. Writing characters down on a piece of paper feels fluid and easy, but once I take a step back and look at the page, it’s incomprehensible at a glance. I have to sound the words out, character by character, if I want to read what I have written.
q7w^jt$ iG· `Bt 81j%j 5`N x`N2^ 1E 7`V2#b% 1b$y6E- y71Tb% a7DzD16R_ 2yY5 5^ `C q`BiFO W qqE6R e`Vj$_ ej`M2% 5#2 `ViD`Û· w1U 5^iO `B 1zDO `C 81qR wzDz 5#2 j`NzH 1E @ qs#O· 1Ti 5%zt^q79V5$8w%jO 1E `C xj5#iO- `B 9r#O 1`N 8`N5&2 @ yuH_ `N1U· a7DzD16R w`Û a7DzD16R· eG `B y5#1 1`N 7`V2# o1E `B 9r#O y71T15$-

However, Tengwar is incredibly pretty. I want to get more practice reading it. What if I could read whatever I want with this writing system? If I only had a script that could convert English text into readable Tengwar for me!
9yYr$6R· 1b$y6E iG 5%z72$w%j`Û q71R1`Û- `B y5#1 1`N s1R t7HO q7zD1iGO 7`V2#b% 1T- o1E eG `B z`Nm& 7`V2# o1Er$6R `B y5#1 y3G 4iG y71Tb% 88Ú1t$À eG `B 5^j`Û 92# `C 8z7qT1 41E z`Nm& z5^r6R1 b$jdT 1zFæ1 5%1`N 7`V2#w#jO 1b$y6E e6Y t`VÁ

As a glance through the Tengwar Textbook will demonstrate, Tengwar is pretty complicated. There isn’t a single standard way to write in English using Tengwar: there are a variety of “modes”, each of which has a different set of rules. I have my own personal way of writing in Tengwar that combines some features of each of those modes that I like.
iD `C xj5#iO 37`Nv& @ 1b$y6E 1zFæ1w`NzH yj%j 2t$5^8171EO· 1b$y6E iG q71R1`Û zt^qjzG1E2$- 47FO iG51 `C 8b%jO 815#2uD y`C`Û 1`N y71TO 5% b$jdT iJb% 1b$y6E- 47FO 7DO `C r7D`B1R`Û W t2^O_· `VaD W oaG 9iD `C 2eGe7F5$1 81R W 7j&O_- `B 9r#O t`Û yY5 q6R85^j# y`C`Û W y71Tb% 5% 1b$y6E 41E zt^w5%O_ 8t^O e`V1E7JO_ W `VaD W 4iHO t2^O_ 41E `B jzGO-

Even though there are already some scripts around the Internet that will claim to transliterate English to Tengwar, they don’t necessarily follow my mode of writing, or even a standard mode. Thus I decided, one evening, to write my own script.
r$5$ 4`Nv& 47FO 7DO j#7`V2#`Û 8t^O 8z7qT1_ 7D`N5&2 @ 5%16R51R 41E yj%j zj`Ct% 1`N 175#8j1T7F1EO b$jdT 1`N 1b$y6E· 4`V`Û 25^1 5iFiF87Dj%`Û ej^jyY t`Û t2^O W y71Tb%· 6Y r$5$ `C 815#2uD t2^O- 3iJ `B 2iF2%2$· 5^O r$5$b%· 1`N y71TO t`Û yY5 8z7qT1-

I like the look of the Tengwar Annatar font, so the script would convert English text to the characters needed to render Tengwar text in that font. Eventually, I may extend it so that I can also output Tengwar using TengwarScript, a TeX package. Writing a script with Tengwar Annatar in mind is the more difficult task of the two because of the way it typesets vowels (tehtar), so adding support for TengwarScript onto the existing script would be easy.
`B jzGO @ j`NzH W @ 1b$y6E 5#51E6E e5^1· 8`N @ 8z7qT1 y`Nm& z5^r6R1 b$jdT 1zFæ1 1`N @ a7DzD16R_ 5`V2$2$ 1`N 75$26R 1b$y6E 1zFæ1 5% 41E e5^1- r$5$1`Mj#j`Û· `B t`C`Û zFæ15$2 1T 8`N 41E `B z5# j#8`N `N1Uq1U 1b$y6E iJb% 1b$y6E8z7qT1· `C 1zFæ qzDzs#O- y71Tb% `C 8z7qT1 y3G 1b$y6E 5#51E6E 5% t5%2 iG @ t7HO 2eGezGj&1 1iDz W @ 1y`N wzF`CiJO W @ y`C`Û 1T 1qÙiF1R_ ryYj$_ Œ19V16Eœ· 8`N 2#2b% 8qUq6Y1 e6Y 1b$y6E8z7qT1 5^1`N @ zFæiG1b% 8z7qT1 y`Nm& w`V `ViD`Û-

As I built this thing and debugged the little errors and inconsistencies that I noticed here and there, I kept track of what it output as the result for the sentence (“This was a triumph. I’m making a note here: huge success!”) that I used for testing. Tengwar has various little complexities – the R-rule, a distinction between voiced and voiceless ‘th’, double consonants like ‘ch’ and ‘ph’ and ‘ng’ and ‘rd’, and vowel carriers – that make correct transliteration more difficult. When put together, the history of my testing string provides a visualization of my progress against these complexities as I improved the script.
iD `B w`Mj%1 4iG 3b% 5#2 2w$x&s2$ @ j1T1jO 6R76Y_ 5#2 5%z5^8iG15$8`B`V_ 41E `B 51YiG2$ 97FO 5#2 47FO· `B zqR1 17zDz W o1E 1T `N1Uq1U iD @ 7iFj&1 e6Y @ 85$15$iO Œ4iG yiD `C 17`Bt&e- `Bt tzDb% `C 51YO 97FO- 9s&O 8zJ8iF_Áœ 41E `B iJ2$ e6Y 1iF1b%- 1b$y6E 9iD r7D`B`NiJ j1T1jO zt^qjzFæ1T`B`V_ @ 6·7j&O· `C 2iG15%z1`B5^ w1Ry`V5$ r`NiG2$ 5#2 r`NiGj$iF_ 3· 2`Nw&jO z5^85^5#1_ jzGO a 5#2 e 5#2 b 5#2 u· 5#2 ryYj$ z6E7`B6R_ 41E tzDO z6Y7zF1 175#8j1T7F1E`B5^ t7HO 2eGezGj&1- o5$ q1U 1s^4$6R· @ 9iG17H`Û W t`Û 1iF1b% 817b% q7r^2%O_ `C riG`Mj#,G1E`B5^ W t`Û q7x^7iF_ x#`C5%81 4iFO zt^qjzFæ1T`B`V_ iD `B t%q7r^2$ @ 8z7qT1-

With the finished product, now I can take my favorite poems and stories, pass them through the transliterator, render the resulting text using the Tengwar Annatar font, and send that document to my Kindle! There are still some little details which could be improved upon, but I’m pleased with the result so far.
y3G @ e5%dT2$ q72^zJ1· 5yY `B z5# 1zDO t`Û er#7H1TO q`Nt$_ 5#2 817H`B`V_· qiD_ 4t$ 37`Nv& @ 175#8j1T7F1E6Y· 75$26R @ 7iFj&1b% 1zFæ1 iJb% @ 1b$y6E 5#51E6E e5^1· 5#2 85$2 41E 2zHt&5$1 1`N t`Û z5%2jOÁ 47FO 7DO 81j%j 8t^O j1T1jO 21R`Cj%_ oaG z`Nm& w`V t%q7r^2$ qU5^· w1U `Bt qj`ViD2$ y3G @ 7iFj&1 8`N e6E-

(english_to_tengwar.py on GitHub Gist)
Œb$jdT·1`N·1b$y6E-q`Û 5^ s3Gw& siG1œ
"""


if __name__ == "__main__":
    # If script is run directly, launch the GUI
    run_gui()
