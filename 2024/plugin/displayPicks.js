// displayPicks.js

fetch('your-api-endpoint')
  .then(response => response.json())
  .then(playerData => {
    const pickList = document.getElementById('pickList');
    const picks = playerData.picks || [];

    picks.forEach(pick => {
      const pickId = pick.id;
      const appearanceId = pick.appearance_id;

      // Create a new <li> element for each pick
      const listItem = document.createElement('li');
      listItem.textContent = `Appearance ID: ${appearanceId}`;

      // Append the <li> element to the pickList <div>
      pickList.appendChild(listItem);
    });
  })
  .catch(error => {
    console.error('Request error:', error);
  });