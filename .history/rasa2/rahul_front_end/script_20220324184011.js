window.onload = (event) => {
    console.log('page is fully loaded');
    function getResponse() {
      let userText = $("#textInput").val();
      let userHtml ='<p class="userText"><span>' +'Me: '+ userText + '</span></p>';
      let botHtml = '<p class="botText"><span>' +'TravelBot: '+ userText + '</span></p>';

      $("#textInput").val("");
      $("#chatbox").append(userHtml);
      $("#chatbox").append(botHtml);
      // document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
  
      // $.get("/get", { msg: userText }).done(function(data) {
      //   let botHtml = '<p class="botText"><span>' + data + '</span></p>';
      //   $("#chatbox").append(botHtml);
      //   document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
      // });
      // let botHtml = '<p class="botText"><span>' + asdfasdf + '</span></p>';
    }
  
    // If enter is pressed, get a response
    $("#textInput").keypress(function(e) {
      if(e.which == 13) {
          getResponse();
      }
    });
  
    // If send button is pressed, get a response
    $("#buttonInput").click(function() {
      getResponse();
    });
  };
  