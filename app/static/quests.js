document.addEventListener('DOMContentLoaded', () => {
    // 1. Handle Subject Toggling (Accordion Logic)
    const headers = document.querySelectorAll('.subject-header');
    
    headers.forEach(header => {
        header.addEventListener('click', (e) => {
            // Prevent toggling if the user clicks the DELETE button
            if (e.target.classList.contains('stop-prop')) return;

            const subjectId = header.getAttribute('data-subject-id');
            const content = document.getElementById(`topics-${subjectId}`);
            const arrow = document.getElementById(`arrow-${subjectId}`);

            if (content.style.display === "none" || content.style.display === "") {
                content.style.display = "block";
                arrow.style.transform = "rotate(180deg)";
            } else {
                content.style.display = "none";
                arrow.style.transform = "rotate(0deg)";
            }
        });
    });
});

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('done-btn')) {
        const topicId = e.target.getAttribute('data-topic-id');
        const subjectId = e.target.getAttribute('data-subject-id');
        const scheduleCard = e.target.closest('div[style*="background"]');

        fetch(`/complete_task/${topicId}`, { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // FIX: Remove the "* 100" because backend already sends 0-100
                    const percentage = Math.round(data.total_progress); 
                    
                    const xpBar = document.getElementById(`progress-fill-${data.subject_id}`);
                    const xpText = document.getElementById(`xp-text-${data.subject_id}`);
                    
                    if (xpBar) xpBar.style.width = percentage + '%';
                    if (xpText) xpText.innerText = percentage;

                    // Cross out the topic on the left list immediately
                    const leftTopicItem = document.getElementById(`topic-item-${topicId}`);
                    if (leftTopicItem) {
                        leftTopicItem.style.opacity = '0.4';
                        leftTopicItem.style.textDecoration = 'line-through';
                        leftTopicItem.style.fontStyle = 'italic';
                    }

                    // Remove from the schedule on the right
                    if (scheduleCard) {
                        scheduleCard.style.opacity = '0';
                        scheduleCard.style.transform = 'translateX(20px)';
                        setTimeout(() => scheduleCard.remove(), 300);
                    }
                }
            })
            .catch(err => console.error("Error:", err));
    }
});


                