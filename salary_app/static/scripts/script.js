const roles = [
        "Hi! I am Ashish — Web Designer",
        "Hi! I am Ashish — Web Developer",
        "Hi! I am Ashish — Data Analyst",
        "Hi! I am Ashish — YouTuber",
        ];

        let roleIndex = 0;

        function typeText(text, element, speed = 100) {
        let i = 0;
        element.text('');
        const typer = setInterval(() => {
            if (i < text.length) {
            element.append(text.charAt(i));
            i++;
            } else {
            clearInterval(typer);
            setTimeout(() => {
                roleIndex = (roleIndex + 1) % roles.length;
                typeText(roles[roleIndex], element, speed);
            }, 2000);
            }
        }, speed);
        }

        $(document).ready(function () {
        const $typewriter = $('#typewriter');
        typeText(roles[roleIndex], $typewriter, 120); // slower speed
        });