/*
 * Cantata
 *
 * Copyright (c) 2011-2022 Craig Drummond <craig.p.drummond@gmail.com>
 *
 * ----
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */

#include "scrobblinglove.h"
#include "scrobbler.h"
#include "support/monoicon.h"
#include "support/utils.h"

static int toggle_love;

ScrobblingLove::ScrobblingLove(QWidget *p)
    : ToolButton(p)
{
    love = MonoIcon::icon(FontAwesome::hearto, Utils::monoIconColor());
    loved = MonoIcon::icon(FontAwesome::heart, Utils::monoIconColor());
    setIcon(love);
    connect(Scrobbler::self(), SIGNAL(loveEnabled(bool)), SLOT(setVisible(bool)));
    connect(Scrobbler::self(), SIGNAL(songChanged(bool)), SLOT(songChanged(bool)));
    connect(Scrobbler::self(), SIGNAL(scrobblerChanged()), SLOT(scrobblerChanged()));
    setVisible(Scrobbler::self()->isLoveEnabled());
    connect(this, SIGNAL(clicked()), this, SLOT(love_function()));
    songChanged(false);
}

void ScrobblingLove::love_function()
{
    if (toggle_love == 0) {
        fprintf(stderr, "sendLove\n");
        Scrobbler::self()->love();
        toggle_love = 1;
        system("mpc_o love");
    } else {
        fprintf(stderr, "sendUnLove\n");
        Scrobbler::self()->unlove();
        toggle_love = 0;
        system("mpc_o unlove");
    }
    scrobblerChanged();
}

void ScrobblingLove::songChanged(bool valid)
{
    setEnabled(valid);
	toggle_love=0;
    love = MonoIcon::icon(FontAwesome::hearto, Utils::monoIconColor());
    setIcon(love);
    setToolTip(tr("%1: Love   Current Track").arg(Scrobbler::self()->activeScrobbler()));
    Scrobbler::self()->loveSent=false;
    Scrobbler::self()->unloveSent=true;
    scrobblerChanged();
}

void ScrobblingLove::scrobblerChanged()
{
    setIcon(isEnabled() && Scrobbler::self()->lovedTrack() ? loved : love);
    setToolTip(isEnabled() && Scrobbler::self()->lovedTrack()
                ? tr("%1: UnLove Current Track").arg(Scrobbler::self()->activeScrobbler())
                : tr("%1: Love   Current Track").arg(Scrobbler::self()->activeScrobbler()));
}

void ScrobblingLove::setloveicon()
{
	toggle_love=1;
    loved = MonoIcon::icon(FontAwesome::heart, Utils::monoIconColor());
    setIcon(loved);
    setToolTip(tr("%1: Unlove Current Track").arg(Scrobbler::self()->activeScrobbler()));
    Scrobbler::self()->loveSent=true;
    Scrobbler::self()->unloveSent=false;
}

void ScrobblingLove::setunloveicon()
{
    love = MonoIcon::icon(FontAwesome::hearto, Utils::monoIconColor());
    setIcon(love);
    setToolTip(tr("%1: Love   Current Track").arg(Scrobbler::self()->activeScrobbler()));
    Scrobbler::self()->loveSent=false;
    Scrobbler::self()->unloveSent=true;
	toggle_love=0;
}

#include "moc_scrobblinglove.cpp"
