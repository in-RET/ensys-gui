"use strict";

function _newArrowCheck(a, b) {
    if (a !== b) throw new TypeError("Cannot instantiate an arrow function")
}

function clearGridModel() {
    var a = this;
    Swal.fire({
        title: "Are you sure?",
        text: "This will clear the whole grid model! This will not actually delete any asset from the scenario. You will need to save after clearing for the changes to actually take effect.",
        icon: "warning",
        showCancelButton: !0,
        confirmButtonText: "Yes, clear everything!",
        cancelButtonText: "Cancel"
    }).then(function (b) {
        return _newArrowCheck(this, a), b.value && editor.clearModuleSelected()
    }.bind(this))
}/* Export Topology to JSON and send to back-end. */
$(".btn-export").click(function () {
    var b = this;// Data Pre-check
    /*
        /* Check if there are duplicate node names in the model
        /* and prevent user from saving the model if there are.
        */
    let c = editor.export().drawflow.Home.data;
    const d = Object.values(c), e = d.map(function (a) {
        return _newArrowCheck(this, b), a.data.name
    }.bind(this)), f = e.filter(function (c, d, e) {
        return _newArrowCheck(this, b), e.indexOf(c) !== d
    }.bind(this));
    if (0 != f.length) return Swal.fire("Grid Model Error", `There are nodes with duplicate names. \n Rename nodes with names: ${f.toString()}`, "error");// End Data Pre-check
    try {
        const a = function (a, c) {
            var d = this;
            _newArrowCheck(this, b);
            const [e, f] = c;
            return a[e] = f.connections.map(function (a) {
                return _newArrowCheck(this, d), "output" in a ? {
                    node: nodesToDB.get("node-" + a.node).uid,
                    output: a.output
                } : {node: nodesToDB.get("node-" + a.node).uid, input: a.input}
            }.bind(this)), a
        }.bind(this), d = Object.values(c).map(function (c) {
            return _newArrowCheck(this, b), {
                db_id: nodesToDB.get("node-" + c.id).uid,
                name: c.name,
                inputs: Object.entries(c.inputs).reduce(a, {}),
                outputs: Object.entries(c.outputs).reduce(a, {}),
                data: c.data,
                pos_x: c.pos_x,
                pos_y: c.pos_y
            }
        }.bind(this));
        $.ajax({
            headers: {"X-CSRFToken": csrfToken},
            type: "POST",
            url: newAssetsCommitTopologyUrl,
            data: JSON.stringify(d),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function () {
                window.location.href = scenarioSearchUrl
            },
            error: function (a) {
                const b = a.responseJSON;
                b.specific_obj_type ? (Swal.fire("Grid Model Error", `Please fill in all ${b.specific_obj_type.bold()} fields. \n
                   Asset ${b.obj_name.bold()} has empty fields or fields with wrong values.`, "error"), console.log(b.full_error)) : Swal.fire("Grid Model Error", `Asset ${b.obj_name.bold()} has empty fields or fields with wrong values.`, "error")
            }
        })
    } catch (a) {
        return console.error("Error while submiting grid model. " + a), Swal.fire("Grid Model Error", "There are empty assets. \n Make sure all assets are filled in with data.", "error")
    }
});