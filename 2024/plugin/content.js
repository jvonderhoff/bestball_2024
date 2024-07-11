// Define an array to store the entryId and appearance_id values
const csvData = [];
const token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNnRTM4R1FUTW1lcVA5djFYVllEUCJ9.eyJ1ZF9zdWIiOiJjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJ1ZF9lbWFpbCI6Imp2b25kZXJob2ZmQGdtYWlsLmNvbSIsInVkX3VzZXJuYW1lIjoianZvbmRlcmhvZmYiLCJpc3MiOiJodHRwczovL3VuZGVyZG9nLnVuZGVyZG9nLmF1dGgwYXBwLmNvbS8iLCJzdWIiOiJhdXRoMHxjOTZlMTM2OS01ZTViLTQyYjktYWUyOC1kYTgzOWNmNWQ1NDMiLCJhdWQiOiJodHRwczovL2FwaS51bmRlcmRvZ2ZhbnRhc3kuY29tIiwiaWF0IjoxNzE4Mjg5Njg4LCJleHAiOjE3MTgyOTMyODgsInNjb3BlIjoib2ZmbGluZV9hY2Nlc3MiLCJndHkiOlsicmVmcmVzaF90b2tlbiIsInBhc3N3b3JkIl0sImF6cCI6ImNRdll6MVQyQkFGYml4NGRZUjM3ZHlEOU8wVGhmMXM2In0.e7uG0_caQWSL2yFZ23rfvZPcjTrAR1OpS8DcHJK65IfKOntClGdiV-NhOZOAPEADUNjFwgA8Vj9cIk4M1hKTYks4PHfYZwvkK0tld8D8pMqI25PU_8f7ziw23Uu6LELIAUW29W6mX4iKCVj-EyIoOYEcc82nGUsdm0y80vnWMhK-xz-QP_iPvNpfj3OnmniNCZfM2OUo15ONgbgOyTr20jxCPFf0msLRNQEIC4kC8ruCkaHRQ-rNtp11GoHc6xn94Vd0rd7RQ99SLzCFknnbc3mLnv9wCWaJxqvJeePgGdr3YMIVja7m5YnURjX6PDkFkYrqPqurWbCaj7FV6-Yf-w';

fetch('https://api.underdogfantasy.com/v3/user/active_drafts', {
  method: 'GET',
  headers: {
    'Authorization': token
  }
})
  .then(response => response.json())
  .then(data => {
    const drafts = data.drafts || [];

    const fetchPromises = drafts.map(draft => {
      const draftId = draft.id;

      return fetch(`https://api.underdogfantasy.com/v2/drafts/${draftId}`, {
        method: 'GET',
        headers: {
          'Authorization': token
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
        });
    });

    Promise.all(fetchPromises)
      .then(() => {
        const csvContent = 'entryId,appearance_id\n' + csvData.map(row => Object.values(row).join(',')).join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
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
      })
      .catch(error => {
        console.error('Request error:', error);
      });
  })
  .catch(error => {
    console.error('Request error:', error);
  });