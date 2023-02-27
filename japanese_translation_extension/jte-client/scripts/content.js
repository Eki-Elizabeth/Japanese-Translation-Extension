function translate(s,cb){
  fetch('http://127.0.0.1:5000/api/translate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    mode: 'cors',
    body: JSON.stringify({
      'text': s 
    })
  }).then(function(r) {
    return r.json(); //先抄，回头再理解，嗯
  }).then(function(data) {
    console.log(data);
    cb(data['text']);
  });
}

//translate(null);
function showTooltip(s){
  var span = document.createElement('span');
  span.classList.add('jte-sel');
  var sel = document.getSelection();
  if (sel && sel.rangeCount) {
      var range = sel.getRangeAt(0).cloneRange();
      // wrap text in span element
      range.surroundContents(span);
      sel.removeAllRanges();
      sel.addRange(range);
      tippy('.jte-sel', {content:s});
      // show tooltip   
  }
}

function playVoice(s){
	new Audio('http://127.0.0.1:5000/api/voice?text='+s).play();
}


document.addEventListener('mouseup', (e) => {
// call showtooltip();
  var s = getSelectedText();
  translate(s,showTooltip);
  playVoice(s);
});

function getSelectedText() {
  if (window.getSelection) {
    return window.getSelection().toString();
  } else if (document.selection) {
    return document.selection.createRange().text;
  }
}
