// Define an array to store the entryId and appearance_id values
const csvData = [];

fetch('https://api.underdogfantasy.com/v3/user/active_drafts', {
  method: 'GET',
  headers: {
    'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNnRTM4R1FUTW1lcVA5djFYVllEUCJ9.eyJ1ZF9zdWIiOiJjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJ1ZF9lbWFpbCI6Imp2b25kZXJob2ZmQGdtYWlsLmNvbSIsInVkX3VzZXJuYW1lIjoianZvbmRlcmhvZmYiLCJpc3MiOiJodHRwczovL3VuZGVyZG9nLnVuZGVyZG9nLmF1dGgwYXBwLmNvbS8iLCJzdWIiOiJhdXRoMHxjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJhdWQiOiJodHRwczovL2FwaS51bmRlcmRvZ2ZhbnRhc3kuY29tIiwiaWF0IjoxNzE4MTYyMTUwLCJleHAiOjE3MTgxNjU3NTAsInNjb3BlIjoib2ZmbGluZV9hY2Nlc3MiLCJndHkiOlsicmVmcmVzaF90b2tlbiIsInBhc3N3b3JkIl0sImF6cCI6ImNRdll6MVQyQkFGYml4NGRZUjM3ZHlEOU8wVGhmMXM2In0.NpFKrTAFvkzasqtk_cofgeIYlAYazcbmvMN0l3Q62C3bGMhyvixQuz5_LCauTjSFF1OJhpSDbpOW4VbEhDS9P7Jvv55t2yZQo4zadY4eB4w1jLeIfqS-17UPTdCQvwsv9O-OjKSwD4jK7acrR7kJIcgalEwEd2revKaGlvfLTEQGGrPQOLUb-C0PuVZn6QpRup1OWIq_IoN4nFZbh1ZcapdvzTbSfVlDZsdmTOl7CELAUIaPjDxKaE9KUedpIdepaF67tFze21Y_XM1aajcHc6BmNteViFeIJd7006yO2L-THBSz5j8Kk8xybcTmVa1Aa44FhP8w0WsMeA8vShiUfQ'
  }
})
  .then(response => response.json())
  .then(data => {
    const drafts = data.drafts || [];

    drafts.forEach(draft => {
      const draftId = draft.id;

      fetch(`https://api.underdogfantasy.com/v2/drafts/${draftId}`, {
        method: 'GET',
        headers: {
          'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNnRTM4R1FUTW1lcVA5djFYVllEUCJ9.eyJ1ZF9zdWIiOiJjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJ1ZF9lbWFpbCI6Imp2b25kZXJob2ZmQGdtYWlsLmNvbSIsInVkX3VzZXJuYW1lIjoianZvbmRlcmhvZmYiLCJpc3MiOiJodHRwczovL3VuZGVyZG9nLnVuZGVyZG9nLmF1dGgwYXBwLmNvbS8iLCJzdWIiOiJhdXRoMHxjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJhdWQiOiJodHRwczovL2FwaS51bmRlcmRvZ2ZhbnRhc3kuY29tIiwiaWF0IjoxNzE4MTYyMTUwLCJleHAiOjE3MTgxNjU3NTAsInNjb3BlIjoib2ZmbGluZV9hY2Nlc3MiLCJndHkiOlsicmVmcmVzaF90b2tlbiIsInBhc3N3b3JkIl0sImF6cCI6ImNRdll6MVQyQkFGYml4NGRZUjM3ZHlEOU8wVGhmMXM2In0.NpFKrTAFvkzasqtk_cofgeIYlAYazcbmvMN0l3Q62C3bGMhyvixQuz5_LCauTjSFF1OJhpSDbpOW4VbEhDS9P7Jvv55t2yZQo4zadY4eB4w1jLeIfqS-17UPTdCQvwsv9O-OjKSwD4jK7acrR7kJIcgalEwEd2revKaGlvfLTEQGGrPQOLUb-C0PuVZn6QpRup1OWIq_IoN4nFZbh1ZcapdvzTbSfVlDZsdmTOl7CELAUIaPjDxKaE9KUedpIdepaF67tFze21Y_XM1aajcHc6BmNteViFeIJd7006yO2L-THBSz5j8Kk8xybcTmVa1Aa44FhP8w0WsMeA8vShiUfQ'
        }
      })
        .then(response => response.json())
        .then(playerData => {
          const draftEntries = playerData.draft.draft_entries || [];
          draftEntries.forEach(entry => {
            const entryId = entry.id;
            const userId = entry.user_id;
            if (userId === "c96e1369-5e5b-42b9-ae28-da839cf5d543") {
              const picks = playerData.draft.picks || [];
              picks.forEach(pick => {
                const pickId = pick.id;
                const draft_entry_id = pick.draft_entry_id;
                if (draft_entry_id === entryId) {
                  const appearanceId = pick.appearance_id;
                  csvData.push({ entryId, appearanceId });
                }
              });
            }
          });
        })
        .catch(error => {
          console.error('Request error:', error);
        })
        .finally(() => {
          // Convert the CSV data to a string
          const csvContent = 'entryId,appearance_id\n' + csvData.map(row => Object.values(row).join(',')).join('\n');
          
          // Create a Blob object from the CSV string
          const blob = new Blob([csvContent], { type: 'text/csv' });

          // Use the browser.downloads API to download the CSV file
          const downloadOptions = {
            url: URL.createObjectURL(blob),
            filename: 'data.csv',
            conflictAction: 'overwrite'
          };

          if (typeof browser !== 'undefined' && browser.downloads && browser.downloads.download) {
            browser.downloads.download(downloadOptions)
              .then(downloadId => {
                console.log('CSV file created successfully. Download ID:', downloadId);
              })
              .catch(error => {
                console.error('Error creating download:', error);
              });
          } else {
            console.error('browser.downloads API is not available.');
          }
        });
    });
  })
  .catch(error => {
    console.error('Request error:', error);
  });