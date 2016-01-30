function fillTable(){
  //head = $(".headertable").detach()
  //$("tbody").empty()
  //$("tbody").append(head)
  $.getJSON('http://electoralstatistics.com/interactives/dii-dw/DII.json', function(data){
    for (e in data){
      $("#mainTable").append("<tr class='entry' id='" + e + "'><td>" + data[e]['firstname'] + " </td><td>" + data[e]['lastname'] + " </td><td>" + data[e]['district'] + " </td><td>" + data[e]['Party'] + " </td><td>" + data[e]['dw'] + " </td><td>" + data[e]['DIIAllAvg'].toFixed(2) + " </td><td>" + data[e]['DIIBillAvg'].toFixed(2) + " </td></tr>")
    }
    sort(2)
  })
    //search(searchstring)
}

function orderTwoAscend(a, b, n){
  if (!(isNaN(parseFloat(a)))){
    return parseFloat(a)-parseFloat(b)
  }
  if (!(isNaN(parseFloat(a.charAt(n))))){
    aN = parseFloat(a.substring(n,a.length))
    bN = parseFloat(b.substring(n,b.length))
    return aN-bN
  }
  else{
    dist = a.charCodeAt(n) - b.charCodeAt(n)
    if (dist == 0){
      return orderTwoAscend(a, b, n+1)
    }
    else {
      if (isNaN(dist)){
        if (isNaN(a.charCodeAt(n))){
          return 47-b.charCodeAt(n)
        }
        if (isNaN(b.charCodeAt(n))){
          return a.charCodeAt(n)-47
        }
      }
      else{
        return dist
      }
    }
  }
}

fields = ['firstname', 'lastname', 'district', 'Party', 'dw', 'DIIAllAvg', 'DIIBillAvg']
function sort(field){
  currentAscend = $("#ascend")
  if (currentAscend.length == 0){
    ascend = true
    currentDescend = $("#descend")
    if (currentDescend.length > 0){
      $("#descend > span").remove()
      currentDescend.removeAttr("id")
    }
  }
  else{
    $("#ascend > span").remove()
    currentAscend.removeAttr("id")
    if (currentAscend.attr("class") == field){
      ascend = false
    }
    else{
      ascend = true
    }
  }
  relTitle = $("." + field).text()
  $("." + field).empty()
  entries = [];
  $('#mainTable > .entry').each(function(){
    entries.push($(this).detach())
  })
  $("#mainTable").empty()
  if (ascend){
    $("." + field).append(relTitle + "<span> &#9652;</span>")
    $("." + field).attr("id", "ascend")
  }
  else{
    $("." + field).append(relTitle + "<span> &#9662;</span>")
    $("." + field).attr("id", "descend")
  }
  entries.sort(function(a, b){
    if (ascend){
      return orderTwoAscend(a.children().eq(field).text(), b.children().eq(field).text(), 0)
    }
    else{
      return (-1) * orderTwoAscend(a.children().eq(field).text(), b.children().eq(field).text(), 0)
    }
  })
  while (entries.length > 0){
    e = entries.shift()
    $("#mainTable").append(e)
    e.click(function(){
      updatePlot($(this).attr('id'))
    })
    }
}

removed = []
counter = 0
function backspace(){
  if ($("#ascend").length > 0){
    currentField = parseInt($("#ascend").attr("class"))
    descend = false
  }
  else{
    currentField = parseInt($("descend").attr("class"))
    descend = true
  }
  lastRemoved = removed.pop()
  for (r in lastRemoved){
    $("#mainTable").append(lastRemoved[r])
  }
  sort(currentField)
  sort(currentField)
  return "finished"
}

function search(searchstring){
  //console.log(searchstring)
  toRemove = []
  $('.entry').each(function(){
    if ($(this).text().toLowerCase().search(searchstring.toLowerCase()) < 0){
      removed.push($(this).detach())
    }
  })
  for (r in removed){
    if (removed[r].text().toLowerCase().search(searchstring.toLowerCase()) >= 0){
      //console.log(removed[r].text())
      $('#mainTable').append(removed[r])
    }
  }
  if ($("#ascend").length > 0){
    currentField = parseInt($("#ascend").attr("class"))
    descend = false
  }
  else{
    currentField = parseInt($("descend").attr("class"))
    descend = true
  }
  sort(currentField)
  sort(currentField)
}

function updatePlot(bioguide){
  $("#chart").attr('src', 'http://electoralstatistics.com/interactives/dii-dw/charts/' + bioguide + '.png')
  $(".selectedEntry").removeAttr("style")
  $(".selectedEntry").attr("class", "entry")
  $("#" + bioguide).attr("class", "entry selectedEntry")
  $("#" + bioguide).attr("style", "font-weight:bold;")
}



headers = $(".headertable > th")
headers.each(function(){
  $(this).click(function(){
    sort(parseInt($(this).attr("class")))
  })
})



$("#search").keyup(function(event){
  //console.log(event.originalEvent.keyCode)
  /*if (event.originalEvent.keyCode==8){
    backspace()
  }*/
  search($("#search").val())
})

fillTable()

