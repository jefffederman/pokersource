<?php
$root = ".";
$title = "poker-engine";
require_once('header.php')
?>

<blockquote>

<h3>poker-eval: poker hand evaluator</h3>

<p>
poker-eval is a C library to evaluate poker hands. The result of the
evalution for a given hand is a number. The general idea is that if
the evalution of your hand is lower than the evaluation of the hand of
your opponent, you lose. Many poker variants are supported (draw,
holdem, omaha, etc.) and more can be added. poker-eval is designed for
speed so that it can be used within poker simulation software using
either exhaustive exploration or Monte Carlo.
</p>

</blockquote>

<?php require_once('footer.php') ?>
