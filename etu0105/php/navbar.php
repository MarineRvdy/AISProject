<nav class="navbar enhanced-navbar">
  <div class="navbar-container">
    <div class="navbar-logo">⚓ AIS Tracker</div>
    <ul class="navbar-menu">
      <li><a href="/index.php" class="<?php echo (basename($_SERVER['PHP_SELF']) == 'index.php' ? 'active' : ''); ?>">Accueil</a></li>
      <li><a href="/ajout_navire.php" class="<?php echo (basename($_SERVER['PHP_SELF']) == 'ajout_navire.php' ? 'active' : ''); ?>">Ajouter navire</a></li>
      <li><a href="/visualiser_navire.php" class="<?php echo (basename($_SERVER['PHP_SELF']) == 'visualiser_navire.php' ? 'active' : ''); ?>">Visualiser navire</a></li>
    </ul>
  </div>
</nav>
