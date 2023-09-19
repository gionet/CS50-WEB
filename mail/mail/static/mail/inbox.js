// document.addEventListener('DOMContentLoaded', function() {

//   // Use buttons to toggle between views
//   document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
//   document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
//   document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
//   document.querySelector('#compose').addEventListener('click', compose_email);

//   // By default, load the inbox
//   load_mailbox('inbox');
// });

// function compose_email() {

//   // Show compose view and hide other views
//   document.querySelector('#emails-view').style.display = 'none';
//   document.querySelector('#compose-view').style.display = 'block';

//   // Clear out composition fields
//   document.querySelector('#compose-recipients').value = '';
//   document.querySelector('#compose-subject').value = '';
//   document.querySelector('#compose-body').value = '';
// }

// function load_mailbox(mailbox) {
  
//   // Show the mailbox and hide other views
//   document.querySelector('#emails-view').style.display = 'block';
//   document.querySelector('#compose-view').style.display = 'none';

//   // Show the mailbox name
//   document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
// }

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submit form
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function view_email_details(id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view_email_details').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    const containerDiv = document.createElement('div');

    // Archive and Unarchive
    // if (email.sender !== currentUserEmail) {
    if (mailbox !== 'sent') {
    
      const reply_btn = document.createElement('button');
      reply_btn.innerHTML = "Reply";
      reply_btn.className = "btn btn-info";
      reply_btn.classList.add('buttons');
      reply_btn.addEventListener('click', function () {
        console.log("REPLY");
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        let subject = email.subject;
        if(subject.split(" ", 1)[0] !== "Re:"){
          subject = "Re: " + email.subject;
        } 
        document.querySelector('#compose-subject').value = subject;
        
        //Create a line of hyphens as separator
        const separator = "-----------------------------------------------------------"
        document.querySelector('#compose-body').value =
        `\n\n${separator}\nOn ${email.timestamp} ${email.sender} wrote:
${email.body}`;
      });
      containerDiv.appendChild(reply_btn);

      const arc_btn = document.createElement('button');
      arc_btn.innerHTML = email.archived ? "Unarchive": "Archive";
      arc_btn.className = email.archived ? "btn btn-danger" : "btn btn-secondary";
      arc_btn.classList.add('buttons');
      arc_btn.addEventListener('click', function () {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => {
          load_mailbox('inbox')
        });
      });
      containerDiv.appendChild(arc_btn);
  }
      
    // ... Display details of the email clicked ...
    const ul = document.createElement('div');
    ul.className = 'list-group';
    ul.classList.add('email-content');
    ul.innerHTML = `
    <div class="d-flex justify-content-between">
      <div class="mb-3">
        <strong>From:</strong> ${email.sender}
      </div>
      <div>
        <span class="text-secondary">${email.timestamp}</span>
      </div>
    </div>
    <div class="mb-3">
      <div><strong>To:</strong> ${email.recipients}</div>
    </div>
    <div class="mb-3">
      <div><strong>Subject:</strong> ${email.subject}</div>
    </div>
      <hr class="col-12">
      <div class=email-body>${email.body}</div>
    </div>
    `;

    containerDiv.appendChild(ul);

    document.querySelector('#view_email_details').innerHTML = '';
    document.querySelector('#view_email_details').appendChild(containerDiv);
    
    // Change read status
    if (!email.read) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }  
  });
};

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view_email_details').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view_email_details').style.display = 'none';
  document.querySelector('#archive').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Iterate emails
    emails.forEach(each_mail => {

      // Print emails
      console.log(each_mail);

    // ... Display each email in rows, overview of all emails ...
    const mail = document.createElement('div');
    mail.className = "list-group-item list-group-item-action border";
    mail.innerHTML = `
    <div class="row">
      <div class="col-auto pr-0">${each_mail.sender}</div>
      <div class="col text-center">Subject: ${each_mail.subject}</div>
      <div class="col-auto pl-0 text-right">${each_mail.timestamp}</div>
    </div>
      `;

    // Change background-color ( read / unread )
    mail.classList.add(each_mail.read ? 'read' : 'unread');

    // Add click event to view email
    mail.addEventListener('click', () => {
      view_email_details(each_mail.id, mailbox);

    });
    document.querySelector('#emails-view').append(mail);
  })
});
}

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });
}

function archive() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view_email_details').style.display = 'none';
  document.querySelector('#archive').style.display = 'block';

}
