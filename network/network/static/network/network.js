// document.addEventListener('DOMContentLoaded', function() {
//     // Some code here
//     let edit_post = false;

//     function EditPost(postId) {
//         editing_post = !editing_post;
//         const postElement = document.getElementById('post-${postId}');
//         const textarea = postElement.querySelector('textarea');

//         if (editing) {

//             textarea.style.display='block';
//             postElement.innerHTML='';
//             postElement.appendChild(textarea);

//         } else {

//             const editedText = textarea.value;

//             postElement.innerHTML = editedText;
//         }
//         }
// });

document.addEventListener('DOMContentLoaded', function() {
    let currentlyEditedPostId = null;
    let originalText = null;
    let textarea = null;
    let editButton = null;

    const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            enterEditingMode(postId);
        });
    });

    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postLikeId = this.dataset.postLikeId;
            likePost(postLikeId, button);
        })
    })
    
    // It enters editing mode for the post with the specified ID.
    function enterEditingMode(postId) {
        console.log(`Editing post with ID: ${postId}`)
        // Exit editing mode for the previously edited post (if any)
        exitEditingMode();

        // Enter editing mode for the clicked post
        currentlyEditedPostId = postId;

        // Get the element for the post with the specified ID.
        var postElement = document.getElementById(`post-${postId}`);
        console.log(`${postId}`)
        
        if (postElement) {
            editButton = document.querySelector(`[data-post-id="${postId}"]`);
            console.log(editButton)
            
            // Hide the edit button.
            if (editButton) {
                editButton.style.visibility = "hidden";
            }

            // Get the original text of the post.
            originalText = postElement.innerText;
            
            // Create a textarea element and set its value to the original text.
            textarea = document.createElement('textarea');
            textarea.value = originalText;

            // Clear the text of the post element.
            postElement.innerText = '';
            
            // Append the textarea element to the post element.
            postElement.appendChild(textarea);

        // Create a "Save" button
        } else {
            console.error(`Post element with ID 'post-${postId}' not found.`);
        }
        
        // Create a save button (HTML) when edit button is clicked.
        const saveButton = document.createElement('button');
        saveButton.textContent = 'Save';
        saveButton.classList.add('btn', 'btn-secondary');

        // When save button is clicked, send to server
        saveButton.addEventListener('click', function(event) {
            event.preventDefault()
            const editedText = textarea.value;
            // Send the editedText to server
            fetch(`post/${postId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    post: editedText
                })
            })
            // Update the postElement(HTML)
            postElement.innerHTML = editedText;
            currentlyEditedPostId = null;

            if (editButton) {
                editButton.style.visibility = "visible";
            }
        });

        // Create a "Cancel" button
        const cancelButton = document.createElement('button');
        cancelButton.type = 'button';
        cancelButton.textContent = 'Cancel';
        cancelButton.classList.add('btn', 'btn-secondary'); // Apply Bootstrap button styling or your custom styles

        // When "Cancel" button is clicked, revert HTML to default
        cancelButton.addEventListener('click', function() {
                postElement.innerHTML = originalText;
                currentlyEditedPostId = null;
                editButton.style.visibility = "visible";
        });

        postElement.appendChild(saveButton);
        postElement.appendChild(cancelButton);
    }

    // Exiting previous edit view (if any)
    // ONLY 1 post is editable at a time.
    function exitEditingMode() {
        if (currentlyEditedPostId !== null) {
            const postElement = document.getElementById(`post-${currentlyEditedPostId}`);
            if (postElement) {
                postElement.innerHTML = originalText;
                currentlyEditedPostId = null;
        
            }
        }
    }

    function likePost(postLikeId, buttonElement) {
    
        const like_button = buttonElement.classList.contains('btn-outline-info');
        const spanElement = document.getElementById(`like-${postLikeId}`);

        let totalLikes = parseInt(spanElement.textContent.trim());

        if (like_button) {
            buttonElement.classList.replace('btn-outline-info', 'btn-info');
            buttonElement.blur();

            totalLikes += 1;
            spanElement.innerHTML = totalLikes

            console.log(totalLikes)

            fetch(`post-like/${postLikeId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    user_like: true
                })
            });
            
        } else {
            buttonElement.classList.replace('btn-info', 'btn-outline-info');
            buttonElement.blur();

            totalLikes -= 1;
            spanElement.innerHTML = totalLikes

            fetch(`post-like/${postLikeId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    user_like: false
                })
            });
        }
            
    }
});
