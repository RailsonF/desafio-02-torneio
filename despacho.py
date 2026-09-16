"""SI Code Week 2026 · Desafio 02 · Torneio de Algoritmos

Escreva a função despachar() abaixo. Não mude o nome nem os parâmetros:
os testes de correção chamam a função exatamente assim.

Regras completas: página do Desafio 02 no sistema da SI Code Week.
Python 3.12, só com a biblioteca padrão.
"""


class _Node:
    __slots__ = ("code", "prev", "next")

    def __init__(self, code):
        self.code = code
        self.prev = None
        self.next = None


def despachar(log: list[str]) -> list[str]:
    """Recebe as linhas do log de despacho e devolve os códigos dos pedidos
    entregues, na ordem em que saíram.

    >>> despachar(["CHEGA P1", "CHEGA P2", "SAI"])
    ['P1']
    """
    head = None
    tail = None
    node_of = {}
    seen = set()
    entregues = []
    hist = []

    _C, _S, _X = 1, 2, 3

    for line in log:
        if "#" in line:
            line = line.split("#", 1)[0]
        line = line.strip()
        if not line:
            continue

        first = line[0]
        if first == "+":
            cmd = "CHEGA"
            rest = line[1:].strip()
            code = rest.split(None, 1)[0].upper() if rest else None
        elif first == "-":
            cmd = "CANCELA"
            rest = line[1:].strip()
            code = rest.split(None, 1)[0].upper() if rest else None
        elif first == ">":
            cmd, code = "SAI", None
        elif first == "<":
            cmd, code = "DESFAZ", None
        else:
            up = line.upper()
            if up == "SAI":
                cmd, code = "SAI", None
            elif up == "DESFAZ":
                cmd, code = "DESFAZ", None
            elif up.startswith("CHEGA"):
                rest = line[5:].strip()
                code = rest.split(None, 1)[0].upper() if rest else None
                cmd = "CHEGA" if code else None
            elif up.startswith("CANCELA"):
                rest = line[7:].strip()
                code = rest.split(None, 1)[0].upper() if rest else None
                cmd = "CANCELA" if code else None
            else:
                cmd, code = None, None

        if cmd is None:
            continue

        if cmd == "CHEGA":
            if code in seen:
                continue
            seen.add(code)
            node = _Node(code)
            if tail is None:
                head = tail = node
            else:
                tail.next = node
                node.prev = tail
                tail = node
            node_of[code] = node
            hist.append((_C, code))

        elif cmd == "SAI":
            if head is None:
                continue
            node = head
            if node.next is None:
                head = tail = None
            else:
                head = node.next
                head.prev = None
            node.prev = node.next = None
            code = node.code
            del node_of[code]
            entregues.append(code)
            hist.append((_S, code))

        elif cmd == "CANCELA":
            node = node_of.get(code)
            if node is None:
                continue
            prevc = node.prev.code if node.prev else None
            nextc = node.next.code if node.next else None
            if node.prev is None:
                head = node.next
            else:
                node.prev.next = node.next
            if node.next is None:
                tail = node.prev
            else:
                node.next.prev = node.prev
            node.prev = node.next = None
            del node_of[code]
            hist.append((_X, code, prevc, nextc))

        else:  # DESFAZ
            if not hist:
                continue
            last = hist.pop()
            kind = last[0]
            if kind == _C:
                code = last[1]
                node = node_of.pop(code)
                seen.discard(code)
                if node.prev is None:
                    head = node.next
                else:
                    node.prev.next = node.next
                if node.next is None:
                    tail = node.prev
                else:
                    node.next.prev = node.prev
            elif kind == _S:
                code = last[1]
                entregues.pop()
                node = _Node(code)
                node.next = head
                if head is None:
                    tail = node
                else:
                    head.prev = node
                head = node
                node_of[code] = node
            else:
                code, prevc, nextc = last[1], last[2], last[3]
                node = _Node(code)
                node.prev = node_of[prevc] if prevc is not None else None
                node.next = node_of[nextc] if nextc is not None else None
                if node.prev is None:
                    head = node
                else:
                    node.prev.next = node
                if node.next is None:
                    tail = node
                else:
                    node.next.prev = node
                node_of[code] = node

    return entregues