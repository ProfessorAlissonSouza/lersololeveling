document.addEventListener("DOMContentLoaded", () => {
    const capitulos = 179; // Número total de capítulos
    const menu = document.querySelector("#menu-capitulos ul");
    const conteudo = document.querySelector("#imagens");
    const btnVoltarTopo = document.querySelector("#btn-voltar-topo");

    // Preenche o menu com os capítulos
    for (let i = 1; i <= capitulos; i++) {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.textContent = `Capítulo ${i}`;
        a.href = `#capitulo-${i}`;
        a.dataset.capitulo = `${String(i).padStart(3, "0")}`;
        a.addEventListener("click", carregarCapitulo);
        li.appendChild(a);
        menu.appendChild(li);
    }

    // Função para carregar as imagens de um capítulo
    function carregarCapitulo(event) {
        event.preventDefault();
        const capitulo = event.target.dataset.capitulo;

        // Limpa o conteúdo atual
        conteudo.innerHTML = "";

        // Carrega as imagens do capítulo
        const basePath = `capítulos/capitulo-${capitulo}/`;

        for (let i = 2; i <= 30; i++) {
            const img = document.createElement("img");
            img.src = `${basePath}${i}.jpg`;
            img.alt = `Página ${i}`;

            img.onload = () => {
                conteudo.appendChild(img);
            };

            img.onerror = () => {
                console.log(`Imagem não encontrada: ${img.src}`);
            };
        }
    }

    // Mostrar o botão "Voltar para o topo" ao rolar a página
    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            btnVoltarTopo.style.display = "block";
        } else {
            btnVoltarTopo.style.display = "none";
        }
    });

    // Voltar para o topo da página ao clicar no botão
    btnVoltarTopo.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});
