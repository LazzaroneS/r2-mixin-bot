import json
from urllib import request
from urllib.parse import urlencode


class Translator(object):
    """A language translator and detector.
    Usage:
    ::
        >>> t = Translator()
        >>> t.translate('hello', from_lang='zh-CN', to_lang='en')
        >>> t.detect("你好")
    """

    # url = "http://translate.google.com/translate_a/t?client=webapp&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1"
    # url = "http://translate.google.com/translate_a/t?client=te&format=html&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1"
    # url = "https://translate.googleapis.com/translate_a/t?anno=3&client=te&format=html&v=1.0&key&tc=1&sr=1&mode=1"
    url = "http://translate.google.com/translate_a/t?client=te&format=html&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1"

    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) "
            "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19"
        ),
    }

    def translate(self, source, from_lang="auto", to_lang="en"):
        """Translate the source text from one language to another."""
        data = {"q": source}
        url = "{url}&sl={from_lang}&tl={to_lang}&hl={to_lang}&tk={tk}".format(
            url=self.url,
            from_lang=from_lang,
            to_lang=to_lang,
            tk=_calculate_tk(source),
        )
        response = self._request(url, data=data)
        result = json.loads(response)
        language = "en"
        if isinstance(result, list):
            try:
                result = result[0]
                language = result[1]
            except IndexError:
                pass
        return result, language

    def detect(self, source):
        """Detect the source text's language."""
        result, language = self.translate(source)
        return language

    def _request(self, url, data=None):
        encoded_data = urlencode(data).encode("utf-8")
        req = request.Request(url=url, headers=self.headers, data=encoded_data)
        resp = request.urlopen(req)
        content = resp.read()
        return content.decode("utf-8")


def _calculate_tk(source):
    """Reverse engineered cross-site request protection."""
    # Source: https://github.com/soimort/translate-shell/issues/94#issuecomment-165433715
    # Source: http://www.liuxiatool.com/t.php

    def c_int(x, nbits=32):
        """C cast to int32, int16, int8..."""
        return (x & ((1 << (nbits - 1)) - 1)) - (x & (1 << (nbits - 1)))

    def c_uint(x, nbits=32):
        """C cast to uint32, uint16, uint8..."""
        return x & ((1 << nbits) - 1)

    tkk = [406398, 561666268 + 1526272306]
    b = tkk[0]

    d = source.encode("utf-8")

    def RL(a, b):
        for c in range(0, len(b) - 2, 3):
            d = b[c + 2]
            d = ord(d) - 87 if d >= "a" else int(d)
            xa = c_uint(a)
            d = xa >> d if b[c + 1] == "+" else xa << d
            a = a + d & 4294967295 if b[c] == "+" else a ^ d
        return c_int(a)

    a = b

    for di in d:
        a = RL(a + di, "+-a^+6")

    a = RL(a, "+-3^+b+-f")
    a ^= tkk[1]
    a = a if a >= 0 else ((a & 2147483647) + 2147483648)
    a %= pow(10, 6)

    tk = "{0:d}.{1:d}".format(a, a ^ b)
    return tk


translater = Translator()
