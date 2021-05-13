var editIndex = 0
var lastEditCommited = -1

function getSelectedText() {
    t = (document.all) ? document.selection.createRange().text : document.getSelection();

    return t;
}

function doSomethingWithSelectedText() {
    // cancel last time highlight
    var selection = getSelectedText();
    var selection_text = selection.toString();
    if (selection_text) {
        if (lastEditCommited != -1) {
            document.getElementById("span" + lastEditCommited).className = "no-highlight"
        }

        let wordField = document.getElementById("note-word")
        wordField.value = selection_text
        var span = document.createElement('SPAN');
        span.textContent = selection_text;
        span.id = "span" + editIndex;
        span.className = "highlight"
        lastEditCommited = editIndex;
        editIndex += 1;

        var range = selection.getRangeAt(0);
        range.deleteContents();
        range.insertNode(span);
    }
}

document.getElementById("note-button").addEventListener("click", saveNote);

function saveNote() {
    lastEditCommited = -1;
    document.getElementById("note-word").value = ""
    document.getElementById("note-definition").value = ""
}



document.onmouseup = doSomethingWithSelectedText;
document.onkeyup = doSomethingWithSelectedText;