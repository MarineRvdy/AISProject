<?php
// Titre de la page
$pageTitle = 'Accueil';

// Inclure l'en-tête
include('php/header.php');
?>

<body>
    <?php include('php/navbar.php'); ?>
    
    <main class="background-img-index home-bg">
        <section class="project-description container">
            <article class="objectif-section card">
                <div class="objectif-content">
                    <h2>
                        <strong>Analyse et Modélisation des Comportements de Navigation<br>
                        des Navires à partir des Données AIS</strong>
                    </h2>
                    <p>
                        Approfondir les compétences acquises dans les modules 
                        <strong><em>Big Data, Intelligence Artificielle, Développement Web</em></strong> 
                        et <strong><em>Base de Données</em></strong> à travers une application complète de traitements et de visualisation de données.
                    </p>
                    <h3>Objectifs Développement Web</h3>
                    <ul class="objectif-list">
                        <li>
                            <strong>Programmation web côté client <span class="tag">front-end</span> :</strong>
                            <ul>
                                <li>Créer une maquette visuelle d’un site web</li>
                                <li>Programmer les éléments de la maquette en <strong>HTML</strong></li>
                                <li>Styliser la maquette en <strong>CSS</strong></li>
                                <li>Dynamiser la page avec <strong>JavaScript</strong></li>
                                <li>Manipuler <strong>AJAX</strong></li>
                            </ul>
                        </li>
                        <li>
                            <strong>Programmation web côté serveur <span class="tag">back-end</span> :</strong>
                            <ul>
                                <li>Créer un code <strong>PHP</strong> pour interagir avec la base de données</li>
                                <li>Traiter et renvoyer les réponses en <strong>PHP</strong></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </article>

            <section class="card">
                <h2 style="text-align:center;">Membres du projet</h2>
                <div class="members-list">
                    <figure class="member">
                        <img src="img/eliott.jpg" alt="Photo de Eliott" />
                        <figcaption>Eliott</figcaption>
                    </figure>
                    <figure class="member">
                        <img src="img/guillaume.jpg" alt="Photo de Guillaume" />
                        <figcaption>Guillaume</figcaption>
                    </figure>
                    <figure class="member">
                        <img src="img/Marine.jpg" alt="Photo de Marine" />
                        <figcaption>Marine</figcaption>
                    </figure>
                </div>
            </section>
        </section>
    </main>

    <?php include('php/footer.php'); ?>
    <script src="js/main.js"></script>
</body>
</html>
