#include "mem/cache/tags/fifo.hh"

#include "debug/CacheRepl.hh"
#include "mem/cache/base.hh"

FIFO::FIFO(const Params *p)
    : BaseSetAssoc(p)
{
}

CacheBlk*
FIFO::accessBlock(Addr addr, bool is_secure, Cycles &lat)
{
    return  BaseSetAssoc::accessBlock(addr, is_secure, lat);
    /*
     * Write your implementation here.
     */
}

CacheBlk*
FIFO::findVictim(Addr addr)
{
    int set = extractSet(addr);
    // grab a replacement candidate
    BlkType *blk = nullptr;
    for (int i = assoc - 1; i >= 0; i--) {
        BlkType *b = sets[set].blks[i];
        if (b->way < allocAssoc) {
            blk = b;
            break;
        }
    }
    assert(!blk || blk->way < allocAssoc);

    if (blk && blk->isValid()) {
        DPRINTF(CacheRepl, "set %x: selecting blk %x for replacement\n",
                set, regenerateBlkAddr(blk->tag, set));
    }

    return blk;
    /*
     * Write your implementation here.
     */
}

void
FIFO::insertBlock(PacketPtr pkt, BlkType *blk)
{
    BaseSetAssoc::insertBlock(pkt, blk);

    int set = extractSet(pkt->getAddr());
    sets[set].moveToHead(blk);
}

void
FIFO::invalidate(CacheBlk *blk)
{
    BaseSetAssoc::invalidate(blk);

    // should be evicted before valid blocks
    int set = blk->set;
    sets[set].moveToTail(blk);
}

FIFO*
FIFOParams::create()
{
    return new FIFO(this);
}
