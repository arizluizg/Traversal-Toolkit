"""Traversal Toolkit web app.  Run:  python app.py  ->  http://127.0.0.1:5000"""
from flask import Flask, jsonify, render_template, request, send_from_directory

from traversal_toolkit import dfa, set_ops, string_extra, text_ops, tree

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/samples")
def samples():
    return send_from_directory("samples", "examples.json")


@app.post("/api/analyze")
def analyze():
    d = request.get_json(force=True) or {}
    has_tree_input = any(d.get(key) not in (None, "") for key in ("pre", "ino", "post"))

    if not has_tree_input:
        src = d.get("dfa_source", "custom")
        text = d.get("dfa_custom", "").strip() if src == "custom" else d.get("dfa", dfa.DEFAULT)
        try:
            return jsonify(dfa=dfa.run(d.get("dfa", dfa.DEFAULT), text))
        except ValueError as e:
            return jsonify(error=str(e)), 400

    try:
        root = tree.build(tree.tokens(d.get("pre", "")), tree.tokens(d.get("ino", "")),
                          tree.tokens(d.get("post", "")))
        trav = {"preorder": tree.preorder(root), "inorder": tree.inorder(root),
                "postorder": tree.postorder(root)}
        join = lambda k: "".join(trav[k])
        a, b = tree.tokens(d.get("set_a", "")), tree.tokens(d.get("set_b", ""))
        da, db = set_ops.default_sets(root)
        src = d.get("dfa_source", "preorder")
        text = d.get("dfa_custom", "").strip() if src == "custom" else join(src)
        str_a_val = join(d.get("str_a", "preorder"))
        str_b_val = join(d.get("str_b", "postorder"))
        return jsonify(
            tree=tree.to_dict(root), inorder=trav["inorder"], summary=tree.summary(root),
            strings=text_ops.string_ops(str_a_val, str_b_val, d.get("find", "")),
            string_extras=string_extra.string_extra_ops(str_a_val, str_b_val),
            sets=set_ops.set_ops(a or da, b or db),
        )
    except (ValueError, KeyError) as e:
        return jsonify(error=str(e) if isinstance(e, ValueError) else "Invalid option."), 400


@app.post("/api/regex")
def regex():
    d = request.get_json(force=True)
    try:
        return jsonify(regex_ops.run(d.get("regex", ""), d.get("text", "")))
    except ValueError as e:
        return jsonify(error=str(e)), 400


if __name__ == "__main__":
    app.run(debug=True)
