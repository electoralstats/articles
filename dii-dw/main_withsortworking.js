function fillTable(){
  $.getJSON('DII.json', function(data){
    for (e in data){
      $("tbody").append("<tr class='entry'><td>" + data[e]['firstname'] + "</td><td>" + data[e]['lastname'] + "</td><td>" + data[e]['district'] + "</td><td>" + data[e]['Party'] + "</td><td>" + data[e]['dw'] + "</td><td>" + data[e]['DIIAllAvg'].toFixed(2) + "</td><td>" + data[e]['DIIBillAvg'].toFixed(2) + "</td>")
    }
  })
}

function orderTwoAscend(a, b, n){
  if (typeof a == "number"){
    return a-b
  }
  else{
    dist = a.charCodeAt(n) - b.charCodeAt(n)
    if (dist == 0){
      return dist = orderTwoAscend(a, b, n+1)
    }
    else {
      return dist
    }
  }
}

fields = ['firstname', 'lastname', 'district', 'Party', 'dw', 'DIIAllAvg', 'DIIBillAvg']
function sort(field, data){
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
  head = $(".headertable").detach()
  $("tbody").empty()
  $("tbody").append(head)
  relTitle = $("." + field).text()
  $("." + field).empty()
  if (ascend){
    $("." + field).append(relTitle + "<span> &#9652;</span>")
    $("." + field).attr("id", "ascend")
  }
  else{
    $("." + field).append(relTitle + "<span> &#9662;</span>")
    $("." + field).attr("id", "descend")
  }
  entries = [];
  $.getJSON('DII.json', function(data){
    for (var i in data){
      entries.push(data[i])
    }
    entries.sort(function(a, b){
      if (ascend){
        return orderTwoAscend(a[fields[field]], b[fields[field]], 0)
      }
      else{
        return (-1) * orderTwoAscend(a[fields[field]], b[fields[field]], 0)
      }
    })
    for (var e in entries){
      $("tbody").append("<tr class='entry'><td>" + entries[e]['firstname'] + "</td><td>" + entries[e]['lastname'] + "</td><td>" + entries[e]['district'] + "</td><td>" + entries[e]['Party'] + "</td><td>" + entries[e]['dw'] + "</td><td>" + entries[e]['DIIAllAvg'].toFixed(2) + "</td><td>" + entries[e]['DIIBillAvg'].toFixed(2) + "</td>")
      }
    }
  );
}

function search(searchstring){
  $('.entry').each(function(){




sort(2)

headers = $("th")
headers.each(function(){
  $(this).click(function(){
    console.log()
    sort(parseInt($(this).attr("class")))
  })
})

searchbox = $("#search")
searchbox.keyup(function(){
  console.log($(this).val())
})
