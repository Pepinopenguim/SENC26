pontos = [(-10,-10), (-10,10), (10,10), (10,-10), (-10,-10)]


def centroide(lista_de_coords):
    xc = 0
    yc = 0
    area = 1

    for i in range(1, len(lista_de_coords)):
        x_antes, y_antes = lista_de_coords[i-1]
        x_depois, y_depois = lista_de_coords[i]

        mult = (x_antes * y_depois - x_depois * y_antes)
        
        xc += mult * (x_antes + x_depois)
        yc += mult * (y_antes + y_depois)

    xc /= 6 * area
    yc /= 6 * area

    return xc, yc


