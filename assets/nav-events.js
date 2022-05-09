"use strict";

function myFunction() {
    let menuToggle = document.getElementById('menu-toggle');
    let mobileNav = document.getElementById('mobile-nav');
    let mobileNavShadow = document.getElementById('mobile-nav-shadow');
    let topHeader = document.getElementById('top-header');

    let pageContent = document.getElementById('page-content');
    if(menuToggle && mobileNav && mobileNavShadow) {
        addListeners(
            menuToggle, mobileNav, 
            mobileNavShadow, topHeader, 
            pageContent
        );
        clearInterval(refreshID);
    }
}

let refreshID = setInterval(myFunction, 250);

function addListeners(
    menuToggle, mobileNav, mobileNavShadow, 
    topHeader, pageContent
) {
    let isThrottling = false;
    [mobileNav, menuToggle].forEach((mobEl) => {
        mobEl.addEventListener('click', () => {
            if (isThrottling) {
                return;
            }
            if (mobileNav.classList.contains('active')) {
                isThrottling = true;
                setTimeout(
                    () => {
                        mobileNavShadow.classList.toggle('active')
                        mobileNav.classList.toggle('active')
                        isThrottling = false;
                        topHeader.classList.toggle('top-header-fixed');
                        pageContent.classList.toggle('extra-margin-for-header');
                    },
                    1000
                );
                window.requestAnimationFrame(tstamp => rightStep(tstamp, mobileNav));
                window.requestAnimationFrame(tstamp => downOpacity(tstamp, mobileNavShadow));
            } else {
                topHeader.classList.toggle('top-header-fixed');
                pageContent.classList.toggle('extra-margin-for-header');
                isThrottling = true;
                setTimeout(
                    () => {
                        isThrottling = false;
                    },
                    1000
                );
                mobileNavShadow.classList.toggle('active');
                mobileNav.classList.toggle('active');
                window.requestAnimationFrame(tstamp => leftStep(tstamp, mobileNav));
                window.requestAnimationFrame(tstamp => upOpacity(tstamp, mobileNavShadow));
            }
        });
    });
    
    window.addEventListener('resize', () => {
        if (isThrottling) {
            return;
        }
        if (mobileNav.classList.contains('active') && window.innerWidth > 700) {
            isThrottling = true;
            setTimeout(
                () => {
                    mobileNavShadow.classList.toggle('active')
                    mobileNav.classList.toggle('active')
                    isThrottling = false;
                },
                1000
            );
            window.requestAnimationFrame(tstamp => rightStep(tstamp, mobileNav));
            window.requestAnimationFrame(tstamp => downOpacity(tstamp, mobileNavShadow));
        }
    });
}

let start;

function leftStep(timestamp, el) {
    if (start === undefined)
      start = timestamp;
    const elapsed = timestamp - start;
  
    // `Math.min()` is used here to make sure that the element stops at exactly 50vw.
    let vwWal = Math.max(100 - 0.2 * elapsed, 50)
    el.style.left = vwWal + 'vw';
  
    if (elapsed < 1000 || vwWal > 50) { // Stop the animation after 1 second
        window.requestAnimationFrame(tstamp => leftStep(tstamp, el));
    } else {
        start = undefined;
    }
}
 
function rightStep(timestamp, el) {
    if (start === undefined)
      start = timestamp;
    const elapsed = timestamp - start;
  
    // `Math.min()` is used here to make sure that the element stops at exactly 100vw.
    let vWval = Math.min(50 + 0.2 * elapsed, 100);
    el.style.left = vWval + 'vw';

    if (elapsed < 1000 || vWval < 100) { 
        window.requestAnimationFrame(tstamp => rightStep(tstamp, el));
    } else {
        start = undefined;
    }
}

let opStart;

function upOpacity(timestamp, el) {
    if (opStart === undefined)
        opStart = timestamp;
    const elapsed = timestamp - opStart;
  
    // `Math.min()` is used here to make sure that the element stops at exactly 0.9.
    let opa = Math.min(0.0018 * elapsed, 0.9);
    el.style.opacity = opa;

    if (elapsed < 500 || opa < 0.9) { 
        window.requestAnimationFrame(tstamp => upOpacity(tstamp, el));
    } else {
        opStart = undefined;
    }
}

function downOpacity(timestamp, el) {
    if (opStart === undefined)
        opStart = timestamp;
    const elapsed = timestamp - opStart;
  
    let opa = Math.max(0.9 - 0.0018 * elapsed, 0);
    el.style.opacity = opa;

    if (elapsed < 500 || opa > 0) { 
        window.requestAnimationFrame(tstamp => downOpacity(tstamp, el));
    } else {
        opStart = undefined;
    }
}