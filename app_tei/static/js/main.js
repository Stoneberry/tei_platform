$(document).ready(
	function() {

		loadDocumentTitles();

		let condition1 = (window.location.pathname == '/corpus');
		if (condition1) {
			getFormItems();
 			// $("form#search-form").submit( catchSearchQuery );
 		}

})


// Вставляет слайдеры в поисковой блок
function getFormItems() {
  // Перехват поисковых запросов
  $("form#search-form").submit( catchSearchQuery );

}

function catchSearchQuery(){

	// let query_values = $('form#search-form').serialize();
	// $.get("/api/documents?" + query_values, function(data) {
	// 	$( "#list-document-examples" ).empty();
	// 	insertDocuments(data);
 // 	});

    let query_values = $('form#search-form').serialize();
    var cur_api_url = "/api/documents?" + query_values;

    console.log(query_values);
    console.log(cur_api_url);
   
	$.ajax({
  		url: cur_api_url,
  		type: 'GET',
  		jsonp: 'callback',
		success: function( data ) {
			let resRow = $( "#list-document-examples" );
			resRow.empty();
			insertDocuments(data);
    	},
  		error: function(xhr, status, error) {
        	console.log(status + '; ' + error);
        }  		
	});


return false;
}


function insertDocuments(data){
	 for(var doc_id in data) {
		insertDocument(doc_id, data[doc_id]);
	};
}


function insertDocument(doc_id, doc_info){

	let link = "document/" + doc_id;

	var constr1 = `
		<li class="list-group-item border mb-4 d-flex justify-content-between align-items-start">
			<div class="ms-2 me-auto">
				<div class="fw-bold">
					<a class="" href="
	`;


	var person = ` <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
  <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
</svg>`

	var date = 	`<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar" viewBox="0 0 16 16">
  <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
</svg>`

	var description = ` <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-card-text" viewBox="0 0 16 16">
  <path d="M14.5 3a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h13zm-13-1A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-13z"/>
  <path d="M3 5.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5zM3 8a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9A.5.5 0 0 1 3 8zm0 2.5a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5z"/>
</svg>`

	constr1 += link + '" target="_blank">' + doc_info['title'] + '</p></div>';
	constr1 += `<p><span class="fst-italic">` + person + ` Author:</span> ` + doc_info['author_name'] + '</p>';
	constr1 += `<p><span class="fst-italic">` + date + ` Date: </span>` + doc_info['publish_date'] + '</p>';
	constr1 += `<p><span class="fst-italic">` + description + ` Description: </span> ` + doc_info['description'] + '</p></div>';

	if (doc_info["html_format"] === 1){
		constr1 += `<span class="badge bg-secondary rounded-pill">html</span>`;
	};
	if (doc_info["docx_format"] === 1){
		constr1 += `<span class="badge bg-warning text-dark rounded-pill">docx</span>`;
	};
	if (doc_info["xml_format"] === 1){
		constr1 += `<span class="badge badge bg-danger rounded-pill">xml</span>`;
	};

	constr1 += `</li>`;
	$("#list-document-examples").append(constr1);
}


function loadDocumentTitles (){

	$.get("/api/documents", function(data) {

		var documentTitles = new Set();
		for(var key in data) {
			documentTitles.add( data[key]['title'] );
		};
		documentTitles = Array.from(documentTitles);


		// don't navigate away from the field on tab when selecting an item
		$( "#select-title" ).on( "keydown", function( event ) {
			if ( event.keyCode === $.ui.keyCode.TAB &&
				$( this ).autocomplete( "instance" ).menu.active ) {
				event.preventDefault();
			}
		})


		// delegate back to autocomplete, but extract the last term
      	.autocomplete({
        	minLength: 0,
        	source: function( request, response ) {
        		response( $.ui.autocomplete.filter(
        			documentTitles, extractLast( request.term ) ) );
        	},

        	// prevent value inserted on focus
        	focus: function() {
        		return false;
        	},

        	select: function( event, ui ) {
        		var terms = split( this.value );
          		// remove the current input
          		terms.pop();
          		// add the selected item
          		terms.push( ui.item.value );
          		// add placeholder to get the comma-and-space at the end
          		terms.push( "" );
          		this.value = terms.join( ", " );
          		return false;
          	}
    	});
	})
}


function getDocumentTitles(acc, item) { 
  let title = item.title;
  acc.push(title); 
  return acc;
}


function split( val ) {
    return val.split( /,\s*/ );
}

function extractLast( term ) {
    return split( term ).pop();
}
