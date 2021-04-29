        function toggleVisibility(event) {
            if (event.getAttribute('showed') === "") {
                event.removeAttribute('showed');
            }
            else {
                event.setAttribute('showed', '');
            }
        }
