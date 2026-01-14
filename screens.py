def draw_game_over(screen, score):
    screen.draw.text(
        "GAME OVER",
        center=(400, 200),
        fontsize=60
    )
    screen.draw.text(
        f"Score: {score}",
        center=(400, 260),
        fontsize=30
    )

def draw_victory(screen, score):
    screen.draw.text(
        "YOU WIN!",
        center=(400, 200),
        fontsize=60
    )
    screen.draw.text(
        f"Score: {score}",
        center=(400, 260),
        fontsize=30
    )
