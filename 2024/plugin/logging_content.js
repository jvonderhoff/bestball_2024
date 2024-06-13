fetch('https://api.underdogfantasy.com/v3/user/active_drafts', {
  method: 'GET',
  headers: {
    'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNnRTM4R1FUTW1lcVA5djFYVllEUCJ9.eyJ1ZF9zdWIiOiJjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJ1ZF9lbWFpbCI6Imp2b25kZXJob2ZmQGdtYWlsLmNvbSIsInVkX3VzZXJuYW1lIjoianZvbmRlcmhvZmYiLCJpc3MiOiJodHRwczovL3VuZGVyZG9nLnVuZGVyZG9nLmF1dGgwYXBwLmNvbS8iLCJzdWIiOiJhdXRoMHxjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJhdWQiOiJodHRwczovL2FwaS51bmRlcmRvZ2ZhbnRhc3kuY29tIiwiaWF0IjoxNzE4MTYyMTUwLCJleHAiOjE3MTgxNjU3NTAsInNjb3BlIjoib2ZmbGluZV9hY2Nlc3MiLCJndHkiOlsicmVmcmVzaF90b2tlbiIsInBhc3N3b3JkIl0sImF6cCI6ImNRdll6MVQyQkFGYml4NGRZUjM3ZHlEOU8wVGhmMXM2In0.NpFKrTAFvkzasqtk_cofgeIYlAYazcbmvMN0l3Q62C3bGMhyvixQuz5_LCauTjSFF1OJhpSDbpOW4VbEhDS9P7Jvv55t2yZQo4zadY4eB4w1jLeIfqS-17UPTdCQvwsv9O-OjKSwD4jK7acrR7kJIcgalEwEd2revKaGlvfLTEQGGrPQOLUb-C0PuVZn6QpRup1OWIq_IoN4nFZbh1ZcapdvzTbSfVlDZsdmTOl7CELAUIaPjDxKaE9KUedpIdepaF67tFze21Y_XM1aajcHc6BmNteViFeIJd7006yO2L-THBSz5j8Kk8xybcTmVa1Aa44FhP8w0WsMeA8vShiUfQ'
  }
})
  .then(response => response.json())
  .then(data => {
    console.log(data);
    const drafts = data.drafts || [];

    drafts.forEach(draft => {
      const draftId = draft.id;
      console.log("Draft ID:", draftId);

      fetch(`https://api.underdogfantasy.com/v2/drafts/${draftId}`, {
        method: 'GET',
        headers: {
          'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNnRTM4R1FUTW1lcVA5djFYVllEUCJ9.eyJ1ZF9zdWIiOiJjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJ1ZF9lbWFpbCI6Imp2b25kZXJob2ZmQGdtYWlsLmNvbSIsInVkX3VzZXJuYW1lIjoianZvbmRlcmhvZmYiLCJpc3MiOiJodHRwczovL3VuZGVyZG9nLnVuZGVyZG9nLmF1dGgwYXBwLmNvbS8iLCJzdWIiOiJhdXRoMHxjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJhdWQiOiJodHRwczovL2FwaS51bmRlcmRvZ2ZhbnRhc3kuY29tIiwiaWF0IjoxNzE4MTYyMTUwLCJleHAiOjE3MTgxNjU3NTAsInNjb3BlIjoib2ZmbGluZV9hY2Nlc3MiLCJndHkiOlsicmVmcmVzaF90b2tlbiIsInBhc3N3b3JkIl0sImF6cCI6ImNRdll6MVQyQkFGYml4NGRZUjM3ZHlEOU8wVGhmMXM2In0.NpFKrTAFvkzasqtk_cofgeIYlAYazcbmvMN0l3Q62C3bGMhyvixQuz5_LCauTjSFF1OJhpSDbpOW4VbEhDS9P7Jvv55t2yZQo4zadY4eB4w1jLeIfqS-17UPTdCQvwsv9O-OjKSwD4jK7acrR7kJIcgalEwEd2revKaGlvfLTEQGGrPQOLUb-C0PuVZn6QpRup1OWIq_IoN4nFZbh1ZcapdvzTbSfVlDZsdmTOl7CELAUIaPjDxKaE9KUedpIdepaF67tFze21Y_XM1aajcHc6BmNteViFeIJd7006yO2L-THBSz5j8Kk8xybcTmVa1Aa44FhP8w0WsMeA8vShiUfQ'
        }
      })
        .then(response => response.json())
        .then(playerData => {
//          console.log(playerData);

          const draftEntries = playerData.draft.draft_entries || [];
          draftEntries.forEach(entry => {
            const entryId = entry.id;
            const userId = entry.user_id;
            if (userId === "c96e1369-5e5b-42b9-ae28-da839cf5d543") {
              console.log("ID:", entryId);
              const picks = playerData.draft.picks || [];
              picks.forEach(pick => {
                const pickId = pick.id;
                const draft_entry_id = pick.draft_entry_id;
                if (draft_entry_id === entryId) {
                  console.log("Appearance ID:", pick.appearance_id);
        }
      });
    }
  });
})
.catch(error => {
  console.error('Request error:', error);
});
    });
  })
  .catch(error => {
    console.error('Request error:', error);
  });