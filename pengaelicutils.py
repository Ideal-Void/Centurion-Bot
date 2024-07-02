#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from time import time


class Stopwatch:
    start_time = 0

    def start(self):
        self.start_time = time()

    def end(self):
        try:
            elapsed = time() - self.start_time
            m = elapsed / 60
            minutes = int(m)
            s = (m - minutes) * 60
            seconds = int(s)
            ms = int(round(s - seconds, 3) * 1000)
            if len(str(minutes)) == 1:
                minutes = f"0{minutes}"
            if len(str(seconds)) == 1:
                seconds = f"0{seconds}"
            if minutes == "00":
                if seconds == "00":
                    return f"{ms}ms"
                return f"{int(seconds)}.{ms} seconds"
            else:
                return f"{minutes}:{seconds}"
        except AttributeError:
            return "The stopwatch was never started."


def list2str(inlist: list, mode: int = 0, add_and: bool = False):
    # if mode == 0: proper sentence formatting (minus period)
    # if mode == 1: remove all separation
    # if mode == 2: remove commas, leaving spaces behind
    # if mode == 3: replace commas and spaces with newlines
    if mode == 1:
        outstr = "".join(inlist)
    else:
        if add_and and len(inlist) > 1:
            inlist.append(inlist[-1])
            inlist[-2] = "and"
        outstr = (
            str(inlist)[1:-1]
            .replace("'", "")
            .replace("\\n", "")  # remove single quotes and newlines
        )
        if add_and:
            if len(inlist) == 3:
                outstr = "".join(outstr.split(","))  # remove all commas
            else:
                outstr = "".join(outstr.rsplit(",", 1))  # remove the last comma
        if mode == 2:
            outstr = outstr.replace(", ", " ")
        elif mode == 3:
            outstr = outstr.replace(", ", "\n")
    return outstr


syllables = [
    "a",
    "ae",
    "ag",
    "ah",
    "al",
    "am",
    "an",
    "art",
    "as",
    "au",
    "av",
    "ayn",
    "az",
    "be",
    "bi",
    "bo",
    "bor",
    "burn",
    "by",
    "ca",
    "cai",
    "car",
    "cat",
    "ce",
    "cei",
    "cer",
    "cha",
    "ci",
    "co",
    "cu",
    "da",
    "dam",
    "dan",
    "del",
    "der",
    "des",
    "di",
    "dil",
    "do",
    "don",
    "dy",
    "dyl",
    "e",
    "el",
    "em",
    "en",
    "ev",
    "ex",
    "fi",
    "fin",
    "finn",
    "fly",
    "fu",
    "ga",
    "go",
    "gor",
    "gy",
    "he",
    "hy",
    "i",
    "ig",
    "il",
    "in",
    "is",
    "iss",
    "ja",
    "ji",
    "jo",
    "jor",
    "ka",
    "kes",
    "kev",
    "kla",
    "ko",
    "lan",
    "lar",
    "ler",
    "li",
    "lo",
    "lu",
    "ly",
    "ma",
    "mar",
    "me",
    "mel",
    "mi",
    "mo",
    "mol",
    "mu",
    "mus",
    "na",
    "nar",
    "ne",
    "nei",
    "no",
    "nor",
    "nos",
    "o",
    "ob",
    "ok",
    "ol",
    "om",
    "on",
    "or",
    "os",
    "pe",
    "pen",
    "per",
    "pu",
    "ra",
    "ral",
    "ran",
    "ras",
    "re",
    "res",
    "rez",
    "ri",
    "rin",
    "rob",
    "ry",
    "sa",
    "sac",
    "sam",
    "san",
    "sans",
    "ser",
    "sey",
    "sha",
    "sky",
    "son",
    "st",
    "str",
    "ta",
    "tam",
    "tay",
    "ter",
    "tha",
    "than",
    "tif",
    "ti",
    "tin",
    "to",
    "tor",
    "tur",
    "u",
    "um",
    "un",
    "ur",
    "va",
    "vac",
    "van",
    "ve",
    "vi",
    "wa",
    "wyn",
    "yu",
    "za",
    "zal",
    "ze",
    "zi",
    "zil",
    "zo",
    "zu",
]

def remove_duplicates(inlist: list):
    return list(dict.fromkeys(inlist))
