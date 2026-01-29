// Handles participant deletion for each activity

document.addEventListener("DOMContentLoaded", () => {
  // Delegate click event for delete icons
  document.getElementById("activities-list").addEventListener("click", async (event) => {
    if (event.target.classList.contains("delete-icon")) {
      const activity = event.target.dataset.activity;
      const email = event.target.dataset.email;
      if (!activity || !email) return;
      if (!confirm(`Unregister ${email} from ${activity}?`)) return;
      try {
        const response = await fetch(`/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`, {
          method: "POST"
        });
        if (response.ok) {
          // Refresh activities
          location.reload();
        } else {
          alert("Failed to unregister participant.");
        }
      } catch (e) {
        alert("Error unregistering participant.");
      }
    }
  });
});
