document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.getElementById('follow-button');
    followButton.addEventListener('click', () => followUnfollow(followButton));
    followButton.addEventListener('mouseover', () => {
        if (followButton.innerHTML.trim() === 'Following') {
            followButton.innerHTML === "Unfollow";
        }
    });
    followButton.addEventListener('mouseout', () => {
        followButton.innerHTML === "Following";
    });
});

function isFollowing(followButton) {
    fetch('/follow')
    .then(response => response.json())
    .then()
}

function followUnfollow(followButton) {
    fetch('/follow', {
        method: 'PUT',
        body: JSON.stringify({
            user_id: followButton.dataset.userId
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        // Update button text based on the result
        if (result.following) {
            followButton.innerHTML = "Following";
        } else {
            followButton.innerHTML = "Follow";
        }
    });
}
