function deleteNote(messaggeId){
  fetch('/delete-message',{
        method:'POST',
        body:JSON.stringify({messaggeId: messaggeId})
  }).then((_res) =>{
      window.location.href='/';
  });
}