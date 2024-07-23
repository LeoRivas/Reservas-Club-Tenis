document.addEventListener('DOMContentLoaded', function () {
    const useTypeField = document.getElementById('use_type');
    const gameTypeField = document.getElementById('game_type');

    if (useTypeField && gameTypeField) {
        const gameTypeDiv = document.getElementById('game_type_div');
        const leagueCategoryDiv = document.getElementById('league_category_div');
        const eliteCategoryDiv = document.getElementById('elite_category_div');
        const academyCategoryDiv = document.getElementById('academy_category_div');
        const player1Div = document.getElementById('player1_div');
        const player2Div = document.getElementById('player2_div');
        const player3Div = document.getElementById('player3_div');
        const player4Div = document.getElementById('player4_div');
        const trainerDiv = document.getElementById('trainer_div');

        function updateFields() {
            const useType = useTypeField.value;
            const gameType = gameTypeField.value;

            if (gameTypeDiv) gameTypeDiv.style.display = 'none';
            if (leagueCategoryDiv) leagueCategoryDiv.style.display = 'none';
            if (eliteCategoryDiv) eliteCategoryDiv.style.display = 'none';
            if (academyCategoryDiv) academyCategoryDiv.style.display = 'none';
            if (player1Div) player1Div.style.display = 'none';
            if (player2Div) player2Div.style.display = 'none';
            if (player3Div) player3Div.style.display = 'none';
            if (player4Div) player4Div.style.display = 'none';
            if (trainerDiv) trainerDiv.style.display = 'none';

            if (useType === 'amistoso') {
                if (gameTypeDiv) gameTypeDiv.style.display = 'block';
                if (gameType === 'singles') {
                    if (player1Div) player1Div.style.display = 'block';
                    if (player2Div) player2Div.style.display = 'block';
                } else if (gameType === 'doubles') {
                    if (player1Div) player1Div.style.display = 'block';
                    if (player2Div) player2Div.style.display = 'block';
                    if (player3Div) player3Div.style.display = 'block';
                    if (player4Div) player4Div.style.display = 'block';
                }
            } else if (useType === 'liga') {
                if (leagueCategoryDiv) leagueCategoryDiv.style.display = 'block';
                if (gameTypeDiv) gameTypeDiv.style.display = 'block';
                if (gameType === 'singles') {
                    if (player1Div) player1Div.style.display = 'block';
                    if (player2Div) player2Div.style.display = 'block';
                } else if (gameType === 'doubles') {
                    if (player1Div) player1Div.style.display = 'block';
                    if (player2Div) player2Div.style.display = 'block';
                    if (player3Div) player3Div.style.display = 'block';
                    if (player4Div) player4Div.style.display = 'block';
                }
            } else if (useType === 'entrenamiento_individual') {
                if (player1Div) player1Div.style.display = 'block';
                if (trainerDiv) trainerDiv.style.display = 'block';
            } else if (useType === 'entrenamiento_grupal') {
                if (player1Div) player1Div.style.display = 'block';
                if (player2Div) player2Div.style.display = 'block';
                if (player3Div) player3Div.style.display = 'block';
                if (player4Div) player4Div.style.display = 'block';
                if (trainerDiv) trainerDiv.style.display = 'block';
            } else if (useType === 'elite') {
                if (eliteCategoryDiv) eliteCategoryDiv.style.display = 'block';
                if (trainerDiv) trainerDiv.style.display = 'block';
            } else if (useType === 'academia_interna') {
                if (academyCategoryDiv) academyCategoryDiv.style.display = 'block';
                if (trainerDiv) trainerDiv.style.display = 'block';
            }
        }

        useTypeField.addEventListener('change', updateFields);
        gameTypeField.addEventListener('change', updateFields);
        updateFields();
    } else {
        console.log('Elements useTypeField or gameTypeField not found, skipping script execution');
    }
});
