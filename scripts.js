selecinados = 0;
numerosSelecionados = [];
//gerarOcorrencias();
function Aciona(id){
  var spanElement = document.getElementById('selecionados');
    var meuElemento = document.getElementById('n'+ id);
    if(meuElemento.style.color == ""){
      if(selecinados < 9){
        meuElemento.style.color = 'rgb(255, 255, 255)';
        meuElemento.style.backgroundColor = 'rgb(32, 152, 105)';
        meuElemento.style.border = '1px';
        
        selecinados = selecinados + 1;

        numerosSelecionados.push(id);

      }
    }else{
      meuElemento.style.color = '';
      meuElemento.style.backgroundColor = '';
      meuElemento.style.border = '';

      selecinados = selecinados - 1;

      var index = numerosSelecionados.indexOf(id);
        if (index !== -1) {
            numerosSelecionados.splice(index, 1);
        }
    }
    spanElement.innerHTML  = selecinados;

  }
  
  function verificaNumeros(){
    if(numerosSelecionados.length > 0){
     // URL = `http://localhost:5000/apis/get-ganhador/${numerosSelecionados}`; // ROTA DO MONGO
      URL = `http://localhost:5000/api/get-ganhador/${numerosSelecionados}`; // ROTA CSV
    fetch(URL)
      .then(response => response.json())
      .then(json => {
        msg = "";
        erro = "";
        if(json.mensagem){
          erro = json.mensagem
        }
        if(json.ganhadores_quadra){
          msg+= "\nVocê teria ganhado na quadra " + json.ganhadores_quadra.length + " veze(s)<br>Na(s) data(s): "
          json.ganhadores_quadra.forEach(function(data) {
            msg+= data + '<br> ';
          });
        }
        if(json.ganhadores_quina){
          msg+= "\nVocê teria ganhado na quina " + json.ganhadores_quina.length + " veze(s)<br>Na(s) data(s): "
          json.ganhadores_quina.forEach(function(data) {
            msg+= data + '<br> ';
          });
        }
        if(json.ganhadores_sena){
          msg+= "\nVocê teria ganhado na sena " + json.ganhadores_sena.length + " veze(s)<br>Na(s) data(s): "
          json.ganhadores_sena.forEach(function(data) {
            msg+= data + '<br> ';
          });
          
        }
        Swal.fire({
          title: msg? "Parabéns" : "Ops",
          html: msg?`<div style="text-align:left">`+msg +`</div>` : erro,
          icon: msg? "success"  : "error"
        });
      })
    }else{
     // alert('Selecione os numeros para verificar');
      Swal.fire({
        title: "Ops",
        text: "Selecione os números para verificar",
        icon: "error"
      });
    }
  }

  function sugerirJogo(){
      //URL = `http://localhost:5000/apis/sugerirJogo/`; // ROTA DO MONGO
      URL = `http://localhost:5000/api/sugerirJogo/`; // ROTA CSV
      fetch(URL)
        .then(response => response.json())
        .then(json => {
          console.log(json)
          var trSugerir = document.getElementById("trSugerir");
          if (trSugerir) {
            var tds = trSugerir.getElementsByTagName("td");
            
            for (var i = 0; i < tds.length; i++) {
              var div = tds[i].getElementsByTagName("div")[0];
                div.innerHTML = json[i];
            }

            const Toast = Swal.mixin({
              toast: true,
              position: "top-end",
              showConfirmButton: false,
              timer: 3000,
              timerProgressBar: true,
              didOpen: (toast) => {
                toast.onmouseenter = Swal.stopTimer;
                toast.onmouseleave = Swal.resumeTimer;
              }
            });
            Toast.fire({
              icon: "success",
              title: "Números gerados. Boa sorte!!!"
            });
        }
        })
}

function gerarOcorrencias(){
  //URL = `http://localhost:5000/apis/getOcorrencias/`; // ROTA DO mongo
  URL = `http://localhost:5000/api/getContagem/`;   // ROTA CSV
  fetch(URL)
    .then(response => response.json())
    .then(json => {
      for(i = 1 ; i <= 10; i++){
      var divOco = document.getElementById("oco"+i);
      if (divOco) {
        var tds = divOco.getElementsByTagName("td");
          var div = tds[0].getElementsByTagName("div")[0];
            div.innerHTML = json[i-1]._id;
            tds[1].innerHTML = "Saiu " + json[i-1].ocorrencias + " vezes";
      }
    }
    })
}
function exibirMais(){  
  //URL = `http://localhost:5000/apis/getOcorrencias/`; // ROTA DO MONGO
  URL = `http://localhost:5000/api/getContagem/`;   // ROTA CSV
  fetch(URL)
    .then(response => response.json())
    .then(json => {
      msg= "";
      for(i = 0 ; i < json.length; i++){
        msg+= (i+1).toString().padStart(2, '0') + "º: " + json[i]._id.toString().padStart(2, '0') + " Saiu "+ json[i].ocorrencias.toString().padStart(3, '0') + "<br>"
      }
     // alert(msg);
      Swal.fire({
        title: "Ocorrência dos números",
        html: msg,
       // icon: "success"
      });
    })
}

function uploadFile() {
  // Capturando o elemento do input de arquivo
  var fileInput = document.getElementById('fileInput');
  // Verificando se um arquivo foi selecionado
  if (fileInput.files.length === 0) {
      alert('Por favor, selecione um arquivo.');
      return;
  }

  // Criando um objeto FormData para enviar os dados do arquivo
  var formData = new FormData();
  formData.append('file', fileInput.files[0]);

  // Configurando a requisição Fetch para enviar o arquivo
  fetch('http://localhost:5000/api/uploader/', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Ocorreu um erro ao enviar o arquivo.');
      }
      return response.json();
  })
  .then(data => {
      alert('Arquivo enviado com sucesso!');
      gerarOcorrencias()
  })
  .catch(error => {
      alert(error.message);
  });
}


