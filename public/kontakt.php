<?php
// Kontaktformular nagroup.biz – sendet Anfragen per E-Mail.
// ---- Einstellungen ----
$RECIPIENT = 'info@nagroup.biz';      // Empfänger der Anfragen
$SENDER    = 'noreply@nagroup.biz';   // Absender (muss auf diesem Server existieren)
$LANGS     = ['de', 'en', 'es', 'zh'];
// -----------------------

$lang = in_array($_POST['lang'] ?? '', $LANGS, true) ? $_POST['lang'] : 'de';
$back = '/' . $lang . '/';

function done($back, $ok) {
    header('Location: ' . $back . ($ok ? '?sent=1' : '?error=1') . '#kontakt', true, 303);
    exit;
}
function clean($s, $max) {
    $s = trim((string)$s);
    $s = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $s);   // keine Header-Injection
    return mb_substr($s, 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /'); exit; }

// Spam-Schutz: verstecktes Feld muss leer sein, Formular nicht schneller als 3 s ausgefüllt
if (!empty($_POST['website'])) done($back, true);
$ts = (int)($_POST['ts'] ?? 0);
if ($ts > 0 && time() - $ts < 3) done($back, true);

$name    = clean($_POST['name'] ?? '', 120);
$company = clean($_POST['company'] ?? '', 160);
$email   = clean($_POST['email'] ?? '', 160);
$message = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 5000);

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) done($back, false);

$subject = '=?UTF-8?B?' . base64_encode('Anfrage über nagroup.biz – ' . $name) . '?=';
$body  = "Neue Anfrage über das Kontaktformular (Sprache: " . strtoupper($lang) . ")\n\n";
$body .= "Name:   $name\nFirma:  $company\nE-Mail: $email\n\n";
$body .= "Nachricht:\n$message\n";
$headers  = "From: NA Group Website <$SENDER>\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";

$ok = mail($RECIPIENT, $subject, $body, $headers, '-f' . $SENDER);
done($back, $ok);
