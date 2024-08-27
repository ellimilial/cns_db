"""
This module reads the dependencies graph and provides a method to regenerate the HTML webpage visualising the connections.
"""
from pathlib import Path

import networkx


def read_graph():
    g = networkx.DiGraph()
    _in_section = None
    with open(Path(__file__).parent / "reference_dependencies.txt") as f:
        for line in f:
            line = line.rstrip("\n")

            # Cytoscape mangles non-ascii characters
            line = line.replace("ń", "n").replace("á", "a").replace("o‐S", "o-S")

            implied = True if len(line.split("//")) > 1 and "implied" in line.split("//")[1].lower() else False
            line = line.split("//")[0].rstrip()
            if len(line) == 0:
                continue
            if line.startswith("-"):
                _in_section = line.split("-")[1].strip().rstrip(":").lower().replace(" ", "_")
                continue

            if _in_section is None:
                if " -> " in line:
                    n1, n2 = line.split(" -> ")
                    g.add_node(n1)
                    g.add_node(n2)
                    g.add_edge(n1, n2)
                    if implied:
                        g.edges[(n1, n2)]["implied"] = True
                else:
                    g.add_node(line)
            else:
                n = line
                g.add_node(n)
                g.nodes[n][_in_section] = True
    return g


def main(only_seed=None):
    g = read_graph()
    print("node #:", len(g.nodes))
    print("edge #:", len(g.edges))
    if only_seed:
        tr = list(networkx.bfs_tree(g, only_seed))
        print(f"Trimming for {len(tr)} dependencies of {only_seed}")
        g = g.subgraph(nodes=tr)

    elements = []
    for n in g.nodes:
        categories = ", ".join([f"'{c}' : true" for c in g.nodes[n] if c])
        elements.append(f"{{data: {{id: '{n}'{', '+ categories if categories else ''}}}}}")
    for e in g.edges:
        implied = ", 'implied': true" if g.edges[e].get('implied') else ''
        elements.append(f"{{data: {{ source: '{e[0]}', target: '{e[1]}'{implied} }}}}")

    # Inject the new elements into the html file in place.
    mark_start = '// START ELEMENTS'
    mark_stop = '// END ELEMENTS'
    with open("reference_dependencies.html") as f:
        html_content = f.read()
        assert mark_start in html_content and mark_stop in html_content

    new_content = "".join([
        html_content[:html_content.index(mark_start)],
        mark_start,
        "\n      " + ",\n      ".join(elements) + "\n",
        "      " + mark_stop,
        html_content[html_content.index(mark_stop) + len(mark_stop):]
    ])
    with open("reference_dependencies.html", "w") as f:
        f.write(new_content)


if __name__ == '__main__':
    main()
    #main("Vilar 2010 (R40)")
