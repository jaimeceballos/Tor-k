
$(document).ready(function() {
 	$('#id_categoria').change(function(event){
        
          var cat= $('#id_categoria').val();
          var toLoad;
  	      if (cat!=''){
              toLoad= 'prod/'+cat+'/';
            }/*else{
              toLoad= 'dpto/'+ idp+'/';
          } */   
          $.get(toLoad, function(data){
                options="" 
               for (var i = 0; i < data.length; i++){
                          
                    options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                }
                $('#id_producto').html(options)
                $("#id_producto option:first").attr('selected', 'selected');
              }, "json");
           });
 });