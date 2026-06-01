/* Cookie consent banner — re9guide.it.com
 * AdSense + Clarity disclosure with EU/UK/CA reject option.
 * Stored in localStorage as 're9guide_consent' = 'accept' | 'reject'.
 */
(function(){
  if (typeof window === 'undefined') return;
  var KEY = 're9guide_consent';
  var existing;
  try { existing = localStorage.getItem(KEY); } catch(e){}
  if (existing === 'accept' || existing === 'reject') return;

  // Detect Korean page
  var isKorean = (document.documentElement.lang || '').toLowerCase().indexOf('ko') === 0
              || (window.location.pathname || '').indexOf('/ko/') >= 0;

  var msg = isKorean
    ? '이 사이트는 콘텐츠 개인화 및 트래픽 분석을 위해 Google AdSense와 Microsoft Clarity 쿠키를 사용합니다. 계속 사용하시면 쿠키 사용에 동의하는 것으로 간주됩니다.'
    : 'This site uses Google AdSense and Microsoft Clarity cookies to personalize content and analyze traffic. By continuing, you agree to our use of cookies.';

  var policyLabel = isKorean ? '개인정보 정책 보기' : 'Privacy Policy';
  var acceptLabel = isKorean ? '동의' : 'Accept';
  var rejectLabel = isKorean ? '거부' : 'Reject';
  var policyHref = isKorean ? '/ko/privacy.html' : '/privacy.html';

  var banner = document.createElement('div');
  banner.id = 're9guide-cookie-consent';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-label', isKorean ? '쿠키 동의' : 'Cookie consent');
  banner.style.cssText = [
    'position:fixed','z-index:99999','left:12px','right:12px','bottom:12px',
    'background:#1a0e0a','border:1px solid #c0392b','border-radius:6px',
    'padding:14px 16px','font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif',
    'font-size:13px','color:#f0ebe8','line-height:1.6',
    'box-shadow:0 4px 18px rgba(0,0,0,0.4)','max-width:980px','margin:0 auto'
  ].join(';');

  banner.innerHTML = ''
    + '<div style="display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">'
    +   '<div style="flex:1;min-width:240px;">'
    +     '<p style="margin:0 0 6px 0;">' + msg + '</p>'
    +     '<a href="' + policyHref + '" style="color:#c0392b;font-size:12px;text-decoration:underline;">' + policyLabel + '</a>'
    +   '</div>'
    +   '<div style="display:flex;gap:8px;flex-shrink:0;">'
    +     '<button id="re9guide-cookie-reject" type="button" style="background:transparent;border:1px solid rgba(192,57,43,0.5);color:#b0a09a;padding:7px 14px;border-radius:3px;font-size:12px;font-family:monospace;cursor:pointer;">' + rejectLabel + '</button>'
    +     '<button id="re9guide-cookie-accept" type="button" style="background:#c0392b;border:1px solid #c0392b;color:#fff;padding:7px 16px;border-radius:3px;font-size:12px;font-family:monospace;font-weight:bold;cursor:pointer;">' + acceptLabel + '</button>'
    +   '</div>'
    + '</div>';

  function attach(){
    if (!document.body) { setTimeout(attach, 50); return; }
    document.body.appendChild(banner);
    document.getElementById('re9guide-cookie-accept').onclick = function(){
      try { localStorage.setItem(KEY, 'accept'); } catch(e){}
      banner.parentNode && banner.parentNode.removeChild(banner);
    };
    document.getElementById('re9guide-cookie-reject').onclick = function(){
      try { localStorage.setItem(KEY, 'reject'); } catch(e){}
      // Best-effort opt-out signals
      try { window['ga-disable-G-XZJHDN44CF'] = true; } catch(e){}
      try { if (window.clarity) window.clarity('stop'); } catch(e){}
      banner.parentNode && banner.parentNode.removeChild(banner);
    };
  }
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', attach);
  } else { attach(); }
})();
